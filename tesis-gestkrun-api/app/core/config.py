from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "GESTKRUN API"
    environment: str = "development"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://gestkrun:gestkrun_dev@localhost:5432/gestkrun"
    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:80"]

    storage_path: str = "/tmp/gestkrun-storage"

    rate_limit_general: int = 100
    rate_limit_auth: int = 20

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
