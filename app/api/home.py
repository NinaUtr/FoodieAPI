from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.config import settings
from app.crud.recipe import RecipeCRUD
from app.db.dependency import get_db


home_router = APIRouter()


@home_router.get("/", status_code=200)
def get_home(request: Request, db: Session = Depends(get_db)):
    return settings.TEMPLATES_PATH.TemplateResponse("index.html", {"request": request, "recipes": RecipeCRUD.get_all(db)})
