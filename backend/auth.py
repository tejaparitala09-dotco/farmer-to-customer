import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import users

SECRET = os.getenv("JWT_SECRET_KEY", "change_this_secret")
EXPIRE = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
bearer = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_token(user):
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user["_id"]), "role": user["role"], "exp": now + timedelta(minutes=EXPIRE)}, SECRET, algorithm="HS256")

def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    if not credentials: raise HTTPException(status_code=401, detail="Authentication required")
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user = users.find_one({"_id": __import__("bson").ObjectId(payload["sub"])})
    except Exception:
        user = None
    if not user: raise HTTPException(status_code=401, detail="Invalid or expired token")
    user["id"] = str(user.pop("_id")); user.pop("password_hash", None)
    return user

def require_role(role):
    def dependency(user=Depends(current_user)):
        if user["role"] != role: raise HTTPException(status_code=403, detail=f"{role.title()} access required")
        return user
    return dependency
