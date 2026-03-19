import datetime
from datetime import datetime, timedelta, timezone
from urllib import request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import UserAlreadyExists, InvalidCredentials, InActiveUser
from app.core.logging import get_logger

logger = get_logger("auth")

class AuthService:
    
    MAX_ATTEMPTS = 5
    LOCK_DURATION_MINUTES = 15
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
            logger.info(f"User registered successfully | id={user.id} | email={user.email} | role={user.role}")
            return user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Failed to register user | email={data.email} | error={str(e)}")
            raise UserAlreadyExists()
    
    def login(self, data: UserLogin, request: Request):
        user = self.db.query(User).filter(User.email == data.email).first()
        now = datetime.now(timezone.utc)

        if not user or not verify_password(data.password, user.password):
            if user:
                user.failed_attempts += 1

                if not user.account_locked_until or user.account_locked_until <= now:
                    self.db.query(User).filter(User.id == user.id).update({
                        "failed_attempts": User.failed_attempts + 1,
                        "account_locked_until": (now + timedelta(minutes=self.LOCK_DURATION_MINUTES))
                        if (user.failed_attempts + 1) >= self.MAX_ATTEMPTS else None
                    })
                    self.db.commit()

            logger.warning(f"Invalid login attempt | email={data.email}")
            raise InvalidCredentials("Invalid email or password.")

        if user.account_locked_until and user.account_locked_until > now:
            logger.warning(f"Account locked login attempt | id={user.id} | email={user.email}")
            raise InvalidCredentials("Account is locked. Please try again later.")

        if not user.is_active:
            logger.warning(f"Inactive user login attempt | id={user.id} | email={user.email}")
            raise InActiveUser()

        user.failed_attempts = 0
        user.account_locked_until = None
        self.db.commit()

        token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
                "ip": request.client.host if request else None,
            }
        )

        logger.info(f"User logged in successfully | id={user.id} | email={user.email} | role={user.role}")
        return token, user