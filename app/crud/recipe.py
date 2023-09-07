from typing import Optional, Sequence
from fastapi import HTTPException
import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Recipe
from app.schemas.recipe import CreateRecipe, UpdateRecipe, SearchRecipe


class RecipeCRUD:

    @staticmethod
    def _check_if_user_can_change_recipe(recipe_submitter_id: int, current_user_id: int):
        if recipe_submitter_id != current_user_id:
            raise HTTPException(status_code=403, detail="You don't have access to this operation.")

    @staticmethod
    def create(db: Session, recipe: CreateRecipe, submitter_id: int) -> Optional[Recipe]:
        new_recipe = Recipe(**recipe.__dict__, submitter_id=submitter_id)
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe

    @staticmethod
    def get(db: Session, recipe_id: int) -> Optional[Recipe]:
        if recipe := db.query(Recipe).filter_by(id=recipe_id).first():
            return recipe
        else:
            raise HTTPException(status_code=404, detail="Not Found")

    def update(self, db: Session, recipe_id: int, recipe: UpdateRecipe, submitter_id: int) -> Optional[Recipe]:
        if old_recipe := self.get(db, recipe_id):
            self._check_if_user_can_change_recipe(old_recipe.submitter_id, submitter_id)
            db.query(Recipe).filter_by(id=recipe_id).update(recipe.__dict__)
            db.commit()
            db.refresh(old_recipe)
            return old_recipe

    def delete(self, db: Session, recipe_id: int, submitter_id: int) -> None:
        if recipe := self.get(db, recipe_id):
            self._check_if_user_can_change_recipe(recipe.submitter_id, submitter_id)
            db.delete(recipe)
            db.commit()

    @staticmethod
    def get_all(db: Session) -> Optional[Sequence[Recipe]]:
        return db.query(Recipe).all()

    @staticmethod
    def search(db: Session, keyword: Optional[str], max_results: int) -> SearchRecipe:
        if keyword:
            recipes = db.query(Recipe).filter(Recipe.label.ilike(f"%{keyword}%")).limit(max_results).all()
        else:
            recipes = db.query(Recipe).limit(max_results).all()
        return SearchRecipe(total_results=len(recipes), results=recipes)

    @staticmethod
    async def get_random_recipe():
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.spoonacular.com/recipes/random?number=1",
                headers={"x-api-key": settings.RANDOM_RECIPE_API_KEY},
            )
        recipe = response.json()
        if recipe.get("status"):
            raise HTTPException(status_code=409, detail="Unable yo get data from api.spoonacular.com")

        return recipe["recipes"][0]


recipe_CRUD = RecipeCRUD()
