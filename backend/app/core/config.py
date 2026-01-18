from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field("Hospital Management System")
    env: str = Field(default="development")
    debug: bool = Field(default=False)
    jwt_secret: str 
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    db_host: str
    db_port: int = 3600
    db_user: str
    db_password: str
    db_name: str

    class Config:
        env_file=".env"
        case_sensitive = False

settings = Settings()