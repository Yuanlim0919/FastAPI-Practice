from datetime import datetime, timedelta
from lib2to3.refactor import RefactoringTool
from msilib import schema
from os import access
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException
import server.models.books as books
from server.AuthConfig.config import settings
from server.AuthConfig.oauth2 import AuthJWT
import server.AuthConfig.utils as utils
import server.AuthConfig.oauth2 as oauth2
from server.db_init import user_collection

router = APIRouter()
Access_Token_Expires_In = settings.Access_Token_Expires_In
Refresh_Token_Expires_In = settings.Refresh_Token_Expires_In

@router.post('/register')
async def create_User(payload:books.CreateUserModel):
    
    user = await user_collection.find_one({'user':payload.user})
    if user:
        raise HTTPException(409,"User already exist!")
    if payload.password != payload.confirm_password:
        raise HTTPException(400,"Password do not match!")
    payload.password = utils.hash_password(payload.password)
    del payload.confirm_password
    result = await user_collection.insert_one(payload.dict())
    temp = await user_collection.find_one({"_id":result.inserted_id})
    new_user = books.CreateResponse(temp)
    return {"status":"success","user":new_user}

@router.post('/login')
async def login(payload:books.LoginUserModel,response:Response,Authorize :AuthJWT = Depends()):
    user = await user_collection.find_one({'user':payload.user})
    if not user: 
        raise HTTPException(400,"Incorrect Username or Password")
    if not utils.verify_password(payload.password,user['password']):
        raise HTTPException(400,"Incorrect Username or Password")

    access_token = Authorize.create_access_token(subject=str(user['_id']), \
                    expires_time=timedelta(minutes=Access_Token_Expires_In))
    refresh_token = Authorize.create_refresh_token(subject=str(user['_id']),\
                    expires_time=timedelta(minutes=Refresh_Token_Expires_In))
    response.set_cookie('access_token',access_token,Access_Token_Expires_In * 60,
                        Access_Token_Expires_In * 60,'/',)
    response.set_cookie('refresh_token',refresh_token,Refresh_Token_Expires_In * 60,
    Refresh_Token_Expires_In * 60,'/')
    return {'access_token':access_token}

@router.get('/refresh')
def refresh_token(response:Response,Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(400,detail="Refresh access key failed!")
        user = user_collection.find_one({'_id':ObjectId(str(user_id))})
        if not user_id:
            raise HTTPException(400,detail="User not exist")
        access_token = Authorize.create_access_token(subject=str(user["id"]),expires_time=timedelta(minutes=Access_Token_Expires_In))
    except Exception as e:
        raise HTTPException(400,detail="Refresh failed")
    response.set_cookie('access_token',access_token,Access_Token_Expires_In*60,Access_Token_Expires_In*60)
    response.set_cookie("logged_in","True",Access_Token_Expires_In*60,Access_Token_Expires_In*60)
    return {'access_token':access_token}


@router.post('/logout')
def logout(response:Response,Authorize:AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in','',-1)
    return {'status':'success'}