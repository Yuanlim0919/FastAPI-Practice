from typing import Optional,Union

from fastapi import Header
from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    title: str = Field(...,minlength=1,max_length=99) #... indicates required, replace with None indicates Optional
    author: str = Field(...,min_length=1,max_length=99)
    year_published: int = Field(...,le=2022) #le: less than or equal

    class Config:
        schema_extra = {
            "example":{
                "title": "The Hobbit",
                "author": "J.R.R. Tolkein",
                "year_published": 1937
            }
        }

class UpdateBookModel(BaseModel):
    title:Optional[str]
    author:Optional[str]
    year_published:Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkein",
                "year_published": 1937
            }
        }

class CreateUserModel(BaseModel):
    user: str = Field(...,min_length=1,max_length=99)
    password:str = Field(...,min_length=8)
    confirm_password:str = Field(...,min_length=8)
    role:Union[str,None] = None

def CreateResponse(user)-> dict:
    return {
        "id":str(user["_id"]),
        "user":user["user"]
    }

class LoginUserModel(BaseModel):
    user:str= Field(...,min_length=1,max_length=99)
    password:str = Field(...,min_length=8)


def ResponseModel(data,message):
    return {
        "data":[data],
        "code":200,
        "message":message
    }

def ErrorResponseModel(error,code,message):
    return {"error":error,"code":code,"message":message}




