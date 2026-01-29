from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Hospital Management System"
    debug: bool = True
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    



    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
