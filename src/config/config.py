from beanie.odm.actions import F
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# from auth import google
# CLOUDINARY_CLOUD_NAME=dmxjhhhfy
# CLOUDINARY_API_KEY=	832751647937789
# CLOUDINARY_API_SECRET=naSmJMa5WnvuPjViaGLNIU0trHY

class Settings(BaseSettings):
    db_link: str = Field(..., env="DB_LINK")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    token_cookie_name: str = Field(..., env="TOKEN_COOKIE_NAME")
    google_client_id: str = Field(..., env="GOOGLE_CLIENT_ID")
    cloudinary_cloud_name: str = Field(..., env="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(..., env="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(..., env="CLOUDINARY_API_SECRET")


    # model_config = SettingsConfigDict(env_file=".env")

    class Config:
        env_file = ".env"
        extra = "ignore" 

settings = Settings()