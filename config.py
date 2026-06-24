import os
from dotenv import load_dotenv

load_dotenv()

class Setting():
    url = os.getenv('URL_DATABASE')
    exp_time: int = os.getenv('EXPIRE_TOKEN_TIME')
    ALGORITHM: str = os.getenv('ALGORITHM')
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    resend_api_key: str = os.getenv('RESEND_API_KEY')
    resend_exp: int = os.getenv('RESEND_KET_EXP')

setting = Setting()
