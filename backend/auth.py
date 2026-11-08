import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv
import bcrypt
from bson import ObjectId
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import users

load_dotenv(Path(__file__).resolve().parent / ".env")
load_dotenv()

SECRET = os.getenv("JWT_SECRET_KEY", "farmer-to-customer-jwt-super-secret-key-32bytes")
EXPIRE = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
bearer = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def create_token(user: dict) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user["_id"]),
        "role": user["role"],
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "exp": now + timedelta(minutes=EXPIRE),
        "iat": now,
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        try:
            query = {"_id": ObjectId(user_id)}
        except Exception:
            query = {"_id": user_id}
        user = users.find_one(query)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired. Please log in again.")
    except Exception:
        user = None

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user["id"] = str(user.pop("_id"))
    user.pop("password_hash", None)
    return user

def require_role(role: str):
    def dependency(user: dict = Depends(current_user)):
        if user.get("role") != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{role.capitalize()} access required"
            )
        return user
    return dependency
