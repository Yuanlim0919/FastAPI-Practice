import base64
from typing import List
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from fastapi import HTTPException,Depends
from bson.objectid import ObjectId
from server.db_init import user_collection
from server.AuthConfig.config import settings

class  Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_Algorithm
    authjwt_decode_algorithms: List[str] = [settings.JWT_Algorithm]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(settings.JWT_Public_Key+'==').decode('utf-8')
    authjwt_private_key: str = base64.b64decode(settings.JWT_Private_Key).decode('utf-8')

@AuthJWT.load_config
def get_config():
    return Settings()

