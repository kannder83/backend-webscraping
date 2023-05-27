from pydantic import BaseSettings


class Settings(BaseSettings):
    # API configuration
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    debug: bool

    # DB configuration
    database_hostname: str
    database_port: int
    database_password: str
    database_username: str

    class Config:
        env_file = ".env"


settings = Settings()
