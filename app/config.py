from pathlib import Path
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseSettings
from starlette.templating import Jinja2Templates


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    JWT_ALGORITHM: str = "HS256"
    DATABASE_URL: str
    JWT_SECRET: str
    OAUTH_SCHEMA = OAuth2PasswordBearer(tokenUrl=f"/auth/login")
    RANDOM_RECIPE_API_KEY: str
    TEMPLATES_PATH: Jinja2Templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


settings = Settings()
