from typing import Optional

from pydantic import BaseModel, EmailStr


class CurrentUser(BaseModel):
    class Config:
        orm_mode = True

    id: int
    first_name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr] = None
    is_superuser: bool = False


class GetUser(BaseModel):
    class Config:
        orm_mode = True

    first_name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr] = None


class CreateUser(BaseModel):
    first_name: Optional[str]
    surname: Optional[str]
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    first_name: Optional[str]
    surname: Optional[str]


class UpdateUserPassword(BaseModel):
    password: str
    new_password: str
    repeated_new_password: str
