from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    user_id: Optional[int] = None
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True
    
class Vote(BaseModel):
    post_id: int
    direction: Annotated[int, Field(strict=True, le=1, ge=-1)]

