from fastapi import Depends
from sqlalchemy.orm.session import Session
from app.config import settings
from app.db.dependency import get_db
from app.exceptions.recipe import RecipeForbiddenException
from app.utils.auth_manager import AuthManager


class RecipeManager(AuthManager):

    def check_access_for_current_user(
            self, recipe_id: int, db: Session = Depends(get_db), token: str = Depends(settings.OAUTH_SCHEMA)
    ):
        current_user = self.get_current_user(db, token)
        current_user_recipe_ids = [recipe.id for recipe in current_user.recipes]
        if recipe_id not in current_user_recipe_ids:
            raise RecipeForbiddenException


recipe_manager = RecipeManager()
