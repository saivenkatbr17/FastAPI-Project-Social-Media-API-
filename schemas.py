from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class Base_Post(BaseModel):
    title: str
    content: str
    published: bool = True

class Cretet_post(Base_Post):
    pass

class Update_post(Base_Post):
    pass

class Post(Base_Post):
    id : int
    #created_at: datetime
    class Config:
        orm_mode = True

class Create_user(BaseModel):
    email: EmailStr
    password: str

class Userout(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
        
class Userlogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_data(BaseModel):
    id: Optional[str] = None
