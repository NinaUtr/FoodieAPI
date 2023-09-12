from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.base import BaseCustomException


class HttpExceptionMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except BaseCustomException as exc:
            return JSONResponse(content={"detail": exc.error_message}, status_code=exc.error_code)
