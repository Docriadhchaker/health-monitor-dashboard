from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql://healthmonitor:healthmonitor@localhost:5432/healthmonitor"
    redis_url: str = "redis://localhost:6379/0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
