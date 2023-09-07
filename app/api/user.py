from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.crud.user import user_CRUD
from app.db.dependency import get_db
from app.schemas.user import CreateUser, GetUser, UpdateUser, UpdateUserPassword
from app.utils.auth_manager import auth_manager

user_router = APIRouter()


@user_router.post("/", status_code=201, response_model=GetUser)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    return user_CRUD.create(db=db, user=user)


@user_router.get("/{user_id}/", status_code=200, response_model=GetUser)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    check_access=Depends(auth_manager.check_access_for_current_user)
):
    return user_CRUD.get(db=db, user_id=user_id)


@user_router.put("/{user_id}/", status_code=200, response_model=GetUser)
def update_user(
    user_id: int,
    user: UpdateUser,
    db: Session = Depends(get_db),
    check_access=Depends(auth_manager.check_access_for_current_user)
):
    return user_CRUD.update(db=db, user_id=user_id, user=user)


@user_router.delete("/{user_id}/", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    check_access=Depends(auth_manager.check_access_for_current_user)
):
    return user_CRUD.delete(db=db, user_id=user_id)


@user_router.put("/{user_id}/update_password", status_code=200, response_model=GetUser)
def update_user_password(
    user_id: int,
    user: UpdateUserPassword,
    db: Session = Depends(get_db),
    check_access=Depends(auth_manager.check_access_for_current_user)
):
    return user_CRUD.update_password(db=db, user_id=user_id, user=user)
