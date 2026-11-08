from fastapi import APIRouter, HTTPException, Depends, status
from pymongo.errors import DuplicateKeyError
from database import users
from models import RegisterRequest, LoginRequest
from auth import hash_password, verify_password, create_token, current_user

router = APIRouter(tags=["auth"])

def public_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "phone": user.get("phone", ""),
        "role": user.get("role", "customer"),
    }

@router.post("/api/auth/register")
def register(data: RegisterRequest):
    user_dict = data.model_dump()
    user_dict["email"] = user_dict["email"].lower().strip()
    raw_password = user_dict.pop("password")
    user_dict["password_hash"] = hash_password(raw_password)

    # Check existing user
    if users.find_one({"email": user_dict["email"]}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    try:
        result = users.insert_one(user_dict)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    user_dict["_id"] = result.inserted_id
    token = create_token(user_dict)
    return {
        "user": public_user(user_dict),
        "token": token,
        "access_token": token,
        "token_type": "bearer",
    }

@router.post("/api/auth/register/{role}")
def register_with_role(role: str, data: RegisterRequest):
    data.role = role
    return register(data)

@router.post("/api/auth/login")
def login(data: LoginRequest):
    email = data.email.lower().strip()
    user = users.find_one({"email": email})
    if not user or not verify_password(data.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_token(user)
    return {
        "user": public_user(user),
        "token": token,
        "access_token": token,
        "token_type": "bearer",
    }

@router.get("/api/auth/me")
def get_me(user: dict = Depends(current_user)):
    return user

@router.get("/api/users/me")
def get_users_me(user: dict = Depends(current_user)):
    return user
