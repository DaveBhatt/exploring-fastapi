from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint # This is used to create a constrained integer type for the dir field in the Vote model, which can only take values of 0 or 1.

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True # This allows Pydantic to read data from SQLAlchemy models using attribute access.


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True # This allows Pydantic to read data from SQLAlchemy models using attribute access.

class PostOut(BaseModel):
    Post: Post
    votes: int
 
    class Config:
        from_attributes = True # This allows Pydantic to read data from SQLAlchemy models using attribute access.


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # This means that the dir field must be an integer with a value of 0 or 1, where 0 represents an unvote and 1 represents a vote. The conint function is used to enforce this constraint on the dir field.