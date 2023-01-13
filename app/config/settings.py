from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseSettings, PostgresDsn


class DefaultSettings(BaseSettings):
    postgres_dealect_driver: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str

    @property
    def db_url(self):
        return PostgresDsn.build(
            scheme=self.postgres_dealect_driver,
            user=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            path=f"/{self.postgres_db or ''}",
        )

    access_token_expire_minutes: int = 60 * 24 * 15  # 15 days
    secret_key: str
    jwt_encode_algorithm = "HS256"
    access_token_url = "api/auth/login"

    @property
    def oauth2(self):
        return OAuth2PasswordBearer(tokenUrl=self.access_token_url)

    emailhunter_api_key: str | None = None
    emailhunter_api_url: str = r"https://api.hunter.io/v2/email-verifier"

    redis_host: str
    redis_port: str

    class Config:
        env_file = ".env"


settings = DefaultSettings()
