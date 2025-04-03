
"""
ENVIRONMENT VARIABLES WAY
"""

# from dotenv import load_dotenv
# import os


# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# SECRET_KEY = os.getenv("SECRET_KEY")



from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str


    model_config = SettingsConfigDict(env_file="/portfolio_project/backend/CourtBookingAPI/.env")


settings = Settings()