import os
from dotenv import load_dotenv

load_dotenv()

class Setting():
    url = os.getenv('URL_DATABASE')

setting = Setting()
