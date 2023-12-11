from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class UserResponse(BaseModel):
    user_id : int = None
    first_name : str = None
    last_name : str = None
    email : str = None
    phonenumber : str = None
    username : str = None
    bio : str = None
    profile_pic :Optional [str]
    created_at : datetime = None
    updated_at : Optional[datetime]

class CreateUserSchema(BaseModel):
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    email : Optional[str] = None
    phonenumber : Optional[str] = None
    username : Optional[str] = None
    bio : Optional[str] = None
    profile_pic : Optional[str] = None
    password : Optional[str] = None

    class Config:
        json_schema_extra = {
            "example" : {
                "first_name" : "Walter",
                "last_name" : "white",
                "email" : "walterwhite123@gmail.com",
                "phonenumber" : "9887766554",
                "username" : "Heisenberg",
                "bio" : "Stay out of my territory",
                "profile_pic" : "",
                "password" : "Walter@123"
            }
        }

class LoginUser(BaseModel):
    username : str = None
    password : str = None

    class Config:
        json_schema_extra = {
            "example" : {
                "username":"Heisenberg",
                "password":"Walter@123"
            }
        }