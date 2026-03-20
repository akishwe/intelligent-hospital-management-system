from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.deps import get_db, security
from app.modules.auth.schemas import UserCreate, UserLogin, UserResponse, TokenResponse, UserInfo
from app.modules.auth.service import AuthService
from app.core.exceptions import UserAlreadyExists, InvalidCredentials, InActiveUser, TokenExpired, InvalidToken
from fastapi_limiter.depends import RateLimiter
from app.core.security import decode_access_token, create_access_token
from app.modules.auth.models import RefreshToken, User
from jose import JWTError, jwt, ExpiredSignatureError
from app.core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        user = service.register(payload)
        return user
    except UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

@router.post("/login", response_model=TokenResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def login(payload: UserLogin, request: Request, db: Session = Depends(get_db)):
    service = AuthService(db)
    ip_address = request.client.host
    try:
        tokens, user = service.login(payload, ip_address=ip_address)
        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            user=UserInfo.model_validate(user)
        )
    except (InvalidCredentials, InvalidToken) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except InActiveUser as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TokenExpired as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/logout")
def logout(credentials=Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token, db)
    user_id = payload.get("sub")
    jti = payload.get("jti")
    service = AuthService(db)
    service.logout(user_id, jti)
    return {"message": "Logged out successfully"}

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(
            refresh_token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
            audience="hms-users",
            issuer=settings.app_name
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    jti = payload.get("jti")
    user_id = payload.get("sub")

    token_entry = db.query(RefreshToken).filter_by(token=jti).first()
    if not token_entry or token_entry.is_revoked:
        raise HTTPException(status_code=401, detail="Token revoked")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid user")

    access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role
    })

    return {"access_token": access_token}