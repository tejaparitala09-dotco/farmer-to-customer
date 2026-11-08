from fastapi import APIRouter, HTTPException, Depends
from pymongo.errors import DuplicateKeyError
from database import users
from models import RegisterRequest, LoginRequest
from auth import hash_password, verify_password, create_token, current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

def public(user):
    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"], "phone": user.get("phone", ""), "role": user["role"]}

@router.post("/register")
def register(data: RegisterRequest):
    user = data.model_dump(); user["email"] = user["email"].lower(); user["password_hash"] = hash_password(user.pop("password"))
    try: result = users.insert_one(user)
    except DuplicateKeyError: raise HTTPException(409, "Email is already registered")
    user["_id"] = result.inserted_id
    return {"user": public(user), "token": create_token(user)}

@router.post("/login")
def login(data: LoginRequest):
    user = users.find_one({"email": data.email.lower()})
    if not user or not verify_password(data.password, user["password_hash"]): raise HTTPException(401, "Invalid email or password")
    return {"user": public(user), "token": create_token(user)}

@router.get("/me")
def me(user=Depends(current_user)): return user
