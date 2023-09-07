from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app.db.dependency import get_db
from app.schemas.auth import AccessToken
from app.schemas.user import GetUser
from app.utils.auth_manager import auth_manager

auth_router = APIRouter()


@auth_router.post("/login", response_model=AccessToken)
def login(db: Session = Depends(get_db), user_data: OAuth2PasswordRequestForm = Depends()):
    return auth_manager.login(db=db, user_data=user_data)


@auth_router.get("/me", response_model=GetUser)
def read_users_me(current_user: GetUser = Depends(auth_manager.get_current_user)):
    return current_user
