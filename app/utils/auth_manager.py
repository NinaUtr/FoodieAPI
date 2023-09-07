from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from jose import jwt, JWTError
from app.config import settings
from app.crud.user import user_CRUD
from app.db.dependency import get_db
from app.models.user import User
from app.schemas.auth import AccessToken
from app.utils.password_manager import password_manager


class AuthManager:

    @staticmethod
    def _authenticate(email: str, password: str, db: Session) -> Optional[User]:
        user = user_CRUD.get_by_email(db, email)
        if not user:
            return None
        if not password_manager.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def _create_access_token(user_id: int) -> str:
        payload = {
            "type": "access_token",
            "exp": datetime.utcnow() + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
            "user_id": user_id
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

    @staticmethod
    def _decode_access_token(token: str) -> Optional[str]:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM], options={"verify_aud": False})
        user_id = payload.get("user_id")
        return user_id

    def login(self, db: Session, user_data: OAuth2PasswordRequestForm) -> AccessToken:
        if user := self._authenticate(email=user_data.username, password=user_data.password, db=db):
            return AccessToken(access_token=self._create_access_token(user_id=user.id))
        else:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

    def get_current_user(self, db: Session = Depends(get_db), token: str = Depends(settings.OAUTH_SCHEMA)) -> User:
        try:
            user_id = self._decode_access_token(token)
        except JWTError:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
            )

        if user := user_CRUD.get(db, user_id):
            return user
        else:
            raise HTTPException(status_code=400, detail="Incorrect user")

    def check_access_for_current_user(
            self, user_id: int, db: Session = Depends(get_db), token: str = Depends(settings.OAUTH_SCHEMA)
    ):
        current_user = self.get_current_user(db, token)
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You don't have access to this operation.")


auth_manager = AuthManager()
