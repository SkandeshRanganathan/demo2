from typing import Optional

from pydantic import BaseModel, EmailStr


# Base schema: used for both creating and updating
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# Create schema: inherits from base
class PostCreate(PostBase):
    pass


# Update schema: also inherits from base (if you want different validation, customize here)
class PostUpdate(PostBase):
    pass


# Response schema: includes the `id`, returned to the client
class PostResponse(PostBase):
    id: int

    class Config:
        orm_mode = True  # Allows compatibility with SQLAlchemy models


class UserCreate(PostBase):
    email: EmailStr
    password: str


class UserOut(PostBase):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class token(BaseModel):
    access_token: str
    token_type: str


class tokendata(BaseModel):
    id: Optional[str]
