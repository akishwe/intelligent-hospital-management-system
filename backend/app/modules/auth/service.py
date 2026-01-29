from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate, UserLogin
from app.core.security import hash_password, verify_password,create_access_token
from app.core.exceptions import UserAlreadyExists, InvalidCredentials, InActiveUser

class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def register(self, data: UserCreate) -> User:
        hashed_password = hash_password(data.password)
        user = User(
            email=data.email,
            password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,
            role=data.role
        )

        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExists()
    
    def login(self, data: UserLogin):
        user = self.db.query(User).filter(User.email == data.email).first()

        if not user or not verify_password(data.password, user.password):
            raise InvalidCredentials()

        if not user.is_active:
            raise InActiveUser()

        token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )

        return token, user