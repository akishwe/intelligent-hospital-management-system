from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.modules.auth.schemas import UserCreate, UserLogin, UserResponse
from app.modules.auth.service import AuthService
from app.core.exceptions import UserAlreadyExists, InvalidCredentials, InActiveUser

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        user = service.register(payload)
        return user
    except UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
@router.post("/login", response_model=UserResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        user = service.login(payload)
        return user
    except InvalidCredentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except InActiveUser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
