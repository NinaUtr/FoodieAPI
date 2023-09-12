import asyncio
from typing import Optional, Sequence
from fastapi import Depends, Query, APIRouter
from sqlalchemy.orm import Session
from app.crud.recipe import recipe_service
from app.db.dependency import get_db
from app.schemas.recipe import GetRecipe, CreateRecipe, UpdateRecipe, SearchRecipe, RandomRecipe
from app.schemas.user import CurrentUser
from app.utils.recipe_manager import recipe_manager

recipe_router = APIRouter()


@recipe_router.post("/", status_code=201, response_model=GetRecipe)
def create_recipe(
    recipe: CreateRecipe,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(recipe_manager.get_current_user)
):
    return recipe_service.create(db=db, item_create={"submitter_id": current_user.id, **recipe.__dict__})


@recipe_router.get("/{recipe_id}/", status_code=200, response_model=GetRecipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return recipe_service.get(db=db, item_id=recipe_id)


@recipe_router.put("/{recipe_id}/", status_code=200, response_model=GetRecipe)
def update_recipe(
    recipe_id: int,
    recipe: UpdateRecipe,
    db: Session = Depends(get_db),
    check_access=Depends(recipe_manager.check_access_for_current_user)
):
    return recipe_service.update(db=db, item_id=recipe_id, item_update=recipe.__dict__)


@recipe_router.delete("/{recipe_id}/", status_code=204)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    check_access=Depends(recipe_manager.check_access_for_current_user)
):
    return recipe_service.delete(db=db, item_id=recipe_id)


@recipe_router.get("/search", status_code=200, response_model=SearchRecipe)
def search_recipes(
    keyword: Optional[str] = None,
    max_results: Optional[int] = Query(gt=0, default=10),
    db: Session = Depends(get_db)
):
    return recipe_service.search(db=db, keyword=keyword, max_results=max_results)


@recipe_router.get("/random", status_code=200, response_model=Sequence[RandomRecipe])
async def get_random_recipes():
    return await asyncio.gather(
            *[recipe_service.get_random_recipe() for _ in range(3)]
        )
