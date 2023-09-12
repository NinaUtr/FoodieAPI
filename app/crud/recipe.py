from typing import Optional
import httpx
from sqlalchemy.orm import Session
from app.config import settings
from app.crud.base import BaseCRUD
from app.exceptions.recipe import (
    RecipeDoesNotExistException,
    RecipeExternalAPIException
)
from app.models import Recipe
from app.schemas.recipe import SearchRecipe


class RecipeService(BaseCRUD):
    def __init__(self):
        super().__init__()
        self.model = Recipe
        self.does_not_exist_exception = RecipeDoesNotExistException

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
            raise RecipeExternalAPIException

        return recipe["recipes"][0]


recipe_service = RecipeService()
