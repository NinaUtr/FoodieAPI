from fastapi import FastAPI

from app.api.auth import auth_router
from app.api.home import home_router
from app.api.recipe import recipe_router
from app.api.user import user_router

app = FastAPI(title="Foodie API", openapi_url="/openapi.json")

app.include_router(recipe_router, prefix="/recipes", tags=["Recipes"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(home_router, prefix="/home", tags=["Home"])
