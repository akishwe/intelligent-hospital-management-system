from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.modules.auth.models import User, RevokedToken
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
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to register user | email={data.email} | error={str(e)}")
            raise UserAlreadyExists()

    def login(self, data: UserLogin, ip_address: str = None):
        user = self.db.query(User).filter(User.email == data.email).first()
        now = datetime.now(timezone.utc)

        if not user or not verify_password(data.password, user.password):
            if user:
                user.failed_attempts += 1
                if user.failed_attempts >= self.MAX_ATTEMPTS:
                    user.account_locked_until = now + timedelta(minutes=self.LOCK_DURATION_MINUTES)
                    logger.warning(f"Account locked | user_id={user.id}")
                self.db.commit()
            logger.warning(f"Invalid login attempt | email={data.email} | ip={ip_address}")
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
                "ip": ip_address
            }
        )
        logger.info(f"User logged in successfully | id={user.id} | email={user.email} | role={user.role} | ip={ip_address}")
        return token, user

    def logout(self, user_id: str, jti: str):
        revoked = RevokedToken(jti=jti)
        self.db.add(revoked)
        self.db.commit()
        logger.info(f"User logged out | user_id={user_id} | token_jti={jti}")