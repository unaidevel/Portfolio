
"""
ENVIRONMENT VARIABLES WAY
"""

# from dotenv import load_dotenv
# import os


# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# SECRET_KEY = os.getenv("SECRET_KEY")




from pydantic import Basemodel

class Settings(Basemodel):
    SECRET_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
    