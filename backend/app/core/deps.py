from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import SessionLocal
from app.core.security import decode_access_token
from sqlalchemy.orm import Session
from typing import Generator
from typing import List
from datetime import datetime, timezone
from app.core.exceptions import InvalidToken, TokenExpired

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token, db)

    if payload is None:
        raise InvalidToken()

    return payload

def require_roles(allowed_roles: List[str]):
    def dependency(current_user: dict= Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Insufficient permissions")
        return current_user
    return dependency