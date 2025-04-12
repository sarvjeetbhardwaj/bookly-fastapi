from pydantic import BaseModel, Field
import uuid
from datetime import datetime as dt

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

class UserLoginModel(BaseModel):
    email : str = Field(max_length=40)
    password : str = Field(min_length=7)
