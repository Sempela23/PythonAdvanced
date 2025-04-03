from pydantic import BaseModel, EmailStr, HttpUrl


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class Users(BaseModel):
    items: list[User]