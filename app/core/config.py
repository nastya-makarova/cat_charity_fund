from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'

    class Config:
        env_file = '.env'


settings = Settings()