from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import SessionLocal
from app.core.security import decode_access_token
from sqlalchemy.orm import Session
from typing import Generator
from typing import List


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")

    return payload

def require_roles(allowed_roles: List[str]):
    def dependency(current_user: dict= Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Insufficient permissions")
        return current_user
    return dependency