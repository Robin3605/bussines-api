from beanie.odm.actions import F
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# from auth import google


class Settings(BaseSettings):
    #aca se agregan las variables de entorno desde el .env y se pueden reutilisar en difrentes archivos asi:
    # from src.config.config import settings
    # api_key_deepl: str = Field(..., env="API_KEY_DEEPL")
    db_link: str = Field(..., env="DB_LINK")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    token_cookie_name: str = Field(..., env="TOKEN_COOKIE_NAME")
    google_client_id: str = Field(..., env="GOOGLE_CLIENT_ID")


    # model_config = SettingsConfigDict(env_file=".env")

    class Config:
        env_file = ".env"
        extra = "ignore" 

settings = Settings()