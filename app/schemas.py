from pydantic import BaseModel,EmailStr
from datetime import datetime
 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CustomPostResponse(BaseModel):
    message: str
    status: int
    success: bool
    data: Post

class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True