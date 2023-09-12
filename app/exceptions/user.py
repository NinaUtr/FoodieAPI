from app.exceptions.base import BaseCustomException


class UserDoesNotExistException(BaseCustomException):
    ERROR_MESSAGE = "User not found."
    ERROR_CODE = 404


class UserAlreadyExistException(BaseCustomException):
    ERROR_MESSAGE = "User already exist."
    ERROR_CODE = 409


class UserForbiddenException(BaseCustomException):
    ERROR_MESSAGE = "You don't have access to this operation."
    ERROR_CODE = 403


class UserWrongPasswordException(BaseCustomException):
    ERROR_MESSAGE = "Wrong password."
    ERROR_CODE = 409


class UserMismatchedPasswordException(BaseCustomException):
    ERROR_MESSAGE = "New password and repeated new password don't match."
    ERROR_CODE = 409


class UserIncorrectLoginException(BaseCustomException):
    ERROR_MESSAGE = "Incorrect username or password."
    ERROR_CODE = 400


class UserCredentialsException(BaseCustomException):
    ERROR_MESSAGE = "Could not validate credentials."
    ERROR_CODE = 401
