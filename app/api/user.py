from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.crud.user import user_service
from app.db.dependency import get_db
from app.schemas.user import CreateUser, GetUser, UpdateUser, UpdateUserPassword
from app.utils.user_manager import user_manager

user_router = APIRouter()


@user_router.post("/", status_code=201, response_model=GetUser)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    return user_service.create(db=db, item_create=user.__dict__)


@user_router.get("/{user_id}/", status_code=200, response_model=GetUser)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    check_access=Depends(user_manager.check_access_for_current_user)
):
    return user_service.get(db=db, item_id=user_id)


@user_router.put("/{user_id}/", status_code=200, response_model=GetUser)
def update_user(
    user_id: int,
    user: UpdateUser,
    db: Session = Depends(get_db),
    check_access=Depends(user_manager.check_access_for_current_user)
):
    return user_service.update(db=db, item_id=user_id, item_update=user.__dict__)


@user_router.delete("/{user_id}/", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    check_access=Depends(user_manager.check_access_for_current_user)
):
    return user_service.delete(db=db, item_id=user_id)


@user_router.put("/{user_id}/update_password", status_code=200, response_model=GetUser)
def update_user_password(
    user_id: int,
    user: UpdateUserPassword,
    db: Session = Depends(get_db),
    check_access=Depends(user_manager.check_access_for_current_user)
):
    return user_service.update_password(db=db, item_id=user_id, item_update=user)
