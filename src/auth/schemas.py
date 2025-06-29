from pydantic import BaseModel, Field
import uuid
from datetime import datetime as dt
from typing import List
from src.books.schemas import Book
from src.review.schemas import ReviewModel

class UserCreateModel(BaseModel):
    first_name : str
    last_name : str
    username : str = Field(max_length=15)
    email : str = Field(max_length=40)
    password : str = Field(min_length=7)


class UserModel(BaseModel):
    uid : uuid.UUID 
    username: str
    email : str
    first_name : str
    last_name : str
    is_verified: bool
    password_hash : str = Field(exclude=True)
    created_at : dt 
    updated_at : dt
    
class UserBooksModel(UserModel):
    books : List[Book]
    reviews : List[ReviewModel]

class UserLoginModel(BaseModel):
    email : str = Field(max_length=40)
    password : str = Field(min_length=7)

class EmailModel(BaseModel):
    email_addresses : List[str]

class PassWordResetRequestModel(BaseModel):
    email : str

class PasswordResetconfirmModel(BaseModel):
    new_password : str
    confirm_new_password : str