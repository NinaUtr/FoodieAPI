from app.exceptions.base import BaseCustomException


class RecipeDoesNotExistException(BaseCustomException):
    ERROR_MESSAGE = "Recipe not found."
    ERROR_CODE = 404


class RecipeForbiddenException(BaseCustomException):
    ERROR_MESSAGE = "You don't have access to this operation."
    ERROR_CODE = 403


class RecipeExternalAPIException(BaseCustomException):
    ERROR_MESSAGE = "Unable yo get data from api.spoonacular.com."
    ERROR_CODE = 409
