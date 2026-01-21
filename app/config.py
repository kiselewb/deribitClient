from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    TEST_DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/cp_test"
    )

    REDIS_HOST: str
    REDIS_PORT: int

    DERIBIT_API_URL: str = "https://www.deribit.com/api/v2"

    CELERY_BEAT_SCHEDULE_INTERVAL: int = 60

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
