from pydantic import BaseSettings
import os
from dotenv import load_dotenv
class Settings(BaseSettings):
    JWT_Public_Key : str
    JWT_Private_Key : str
    Refresh_Token_Expires_In : int
    Access_Token_Expires_In : int
    JWT_Algorithm : str
    Client_Origin:str

    class Config:
        env_file = '.env'
    
load_dotenv()

settings = Settings(JWT_Public_Key=os.getenv('JWT_Public_Key'),
                    JWT_Private_Key=os.getenv('JWT_Private_Key'),
                    Refresh_Token_Expires_In=os.getenv('Refresh_Token_Expires_In'),
                    Access_Token_Expires_In=os.getenv('Access_Token_Expires_In'),
                    JWT_Algorithm=os.getenv('JWT_Algorithm'),
                    Client_Origin=os.getenv('Client_Origin'))

