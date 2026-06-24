from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from database import DB_session
from datetime import timezone, datetime, timedelta
from config import setting
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from schemas.crud import user_exists_service, fetch_user_email
from schemas.HTTPErrors import *
import resend

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

def create_access_token(user_data: dict):
    to_encode = user_data.copy()
    to_encode.update({'exp': datetime.now(timezone.utc) + timedelta(minutes=int(setting.exp_time))})
    token = jwt.encode(to_encode, key=setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return token

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DB_session):
    try:
        print(token)
        payload = jwt.decode(token, key=setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        username: str = payload.get('sub')
        role: str = payload.get('role')
        id: int = payload.get('id')

        if username is None or role is None or id is None:
            raise InvalidTokenError
        
        user = await user_exists_service(username, db)
        if user is None:
            raise NotFoundError(msg='User Not Found')
        
        return user
    
    except InvalidTokenError:
        raise
    except Exception as ex:
        raise ExceptionError(msg=str(ex))



def create_token_email(email_dict: dict):
    to_encode = email_dict.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(hours=int(setting.resend_exp))})
    token = jwt.encode(to_encode, key=setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return token



async def send_email(email: str, reset_token: str, username: str):

    resend.api_key = setting.resend_api_key

    reset_link = f"https://yourapp.com/reset-password?token={reset_token}"


    html_content = f"""
        <h2>Reset Your Password</h2>
        
        <p>Hello, {username}</p>
        
        <p>We received a request to reset your password. Click the link below to set a new password:</p>
        
        <p><a href="{reset_link}">Reset Password</a></p>
        
        <p>Or copy and paste this link into your browser:</p>
        <p>{reset_link}</p>
        
        <p>This link will expire in 1 hour.</p>
        
        <p>If you didn't request this, please ignore this email.</p>
        
        <br>
        <p>Thanks</p>
        <p>Blog Post Team</p>
        """


    params: resend.Emails.SendParams = {
        'from': 'onboarding@resend.dev',
        'to': email,
        'subject': 'Reset Password',
        'html': html_content
    }

    email = resend.Emails.send(params=params)
    return email

def verify_email_token(token: str):
    payload = jwt.decode(token, key=setting.SECRET_KEY, algorithms=[setting.ALGORITHM], options={'verify_exp': True})
    email: str = payload.get('email')

    if email is None:
        raise InvalidTokenError

    return email

