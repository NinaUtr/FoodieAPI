from fastapi import Depends
from sqlalchemy.orm.session import Session
from app.config import settings
from app.db.dependency import get_db
from app.exceptions.user import UserForbiddenException

from app.managers.auth_manager import AuthManager


class UserManager(AuthManager):

    def check_access_for_current_user(
            self, user_id: int, db: Session = Depends(get_db), token: str = Depends(settings.OAUTH_SCHEMA)
    ):
        current_user = self.get_current_user(db, token)
        if user_id != current_user.id:
            raise UserForbiddenException


user_manager = UserManager()
