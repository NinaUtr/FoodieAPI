from typing import Optional
from sqlalchemy.orm import Session

from app.crud.base import BaseCRUD
from app.exceptions.user import (
    UserDoesNotExistException,
    UserWrongPasswordException,
    UserMismatchedPasswordException,
    UserAlreadyExistException
)
from app.utils.password_manager import password_manager
from app.models import User
from app.schemas.user import UpdateUserPassword


class UserService(BaseCRUD):
    def __init__(self):
        super().__init__()
        self.model = User
        self.does_not_exist_exception = UserDoesNotExistException

    def create(self, db: Session, item_create: dict):
        if db.query(User).filter_by(email=item_create.get("email")).first():
            raise UserAlreadyExistException

        item_create["hashed_password"] = password_manager.hash_password(item_create.get("password"))
        item_create.pop("password")
        return super().create(db, item_create)

    def get_by_email(self, db: Session, user_email: str) -> Optional[User]:
        if user := db.query(User).filter_by(email=user_email).first():
            return user
        else:
            raise self.does_not_exist_exception

    def update_password(self, db: Session, item_id: int, item_update: UpdateUserPassword):
        if item_update.new_password != item_update.repeated_new_password:
            raise UserMismatchedPasswordException

        if user_in_db := self.get(db, item_id):
            if not password_manager.verify_password(item_update.password, user_in_db.hashed_password):
                raise UserWrongPasswordException

            super().update(
                db=db,
                item_id=item_id,
                item_update={"hashed_password": password_manager.hash_password(item_update.new_password)}
            )


user_service = UserService()
