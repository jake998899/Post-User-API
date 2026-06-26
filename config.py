from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    url_database: str
    expire_token_time: int = 30
    ALGORITHM: str = 'HS256'
    SECRET_KEY: str
    RESEND_API_KEY: str
    RESEND_KEY_EXPIRE_TIME: int = 1
    

setting = Setting()
