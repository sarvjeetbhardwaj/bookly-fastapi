from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    JWT_SECRET : str
    JWT_ALGORITHM : str
    REDIS_URL : str = "redis://localhost:6379/0"
    DOMAIN : str

    
    model_config = SettingsConfigDict(
        env_file = '.env',
        extra = 'ignore'
    )

config = Settings()

broker_url = config.REDIS_URL
result_backend = config.REDIS_URL

