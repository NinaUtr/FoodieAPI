from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.utils.password_manager import password_manager
from app.models import User
from app.schemas.user import CreateUser, UpdateUser, UpdateUserPassword


class UserCRUD:
    @staticmethod
    def create(db: Session, user: CreateUser) -> User:
        if db.query(User).filter_by(email=user.email).first():
            raise HTTPException(status_code=409, detail=f"User with email '{user.email}' already exists.")

        hashed_password = password_manager.hash_password(user.password)
        user = user.__dict__
        user.pop("password")

        new_user = User(hashed_password=hashed_password, **user)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get(db: Session, user_id: int) -> Optional[User]:
        if user := db.query(User).filter_by(id=user_id).first():
            return user
        else:
            raise HTTPException(status_code=404, detail="Not Found")

    @staticmethod
    def get_by_email(db: Session, user_email: str) -> Optional[User]:
        if user := db.query(User).filter_by(email=user_email).first():
            return user
        else:
            raise HTTPException(status_code=404, detail="Not Found")

    def update(self, db: Session, user_id: int, user: UpdateUser) -> Optional[User]:
        if old_user := self.get(db, user_id):
            db.query(User).filter_by(id=user_id).update(user.__dict__)
            db.commit()
            db.refresh(old_user)
            return old_user

    def delete(self, db: Session, user_id: int) -> None:
        if user := self.get(db, user_id):
            db.delete(user)
            db.commit()

    def update_password(self, db: Session, user_id: int, user: UpdateUserPassword) -> Optional[User]:
        if user.new_password != user.repeated_new_password:
            raise HTTPException(status_code=409, detail=f"New password and repeated new password don't match.")

        if user_in_db := self.get(db, user_id):
            if not password_manager.verify_password(user.password, user_in_db.hashed_password):
                raise HTTPException(status_code=409, detail=f"Wrong password.")

            db.query(User).filter_by(id=user_id).update(
                {"hashed_password": password_manager.hash_password(user.new_password)}
            )
            db.commit()
            db.refresh(user_in_db)
            return user_in_db


user_CRUD = UserCRUD()
