import jwt
from jwt.exceptions import InvalidTokenError
from datetime import timezone, datetime, timedelta
from core.config import setting
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_hash.verify(password, hashed_pass)


def create_access_token(user_data: dict):
    to_encode = user_data.copy()
    to_encode.update({'exp': datetime.now(timezone.utc) + timedelta(minutes=int(setting.expire_token_time))})
    token = jwt.encode(to_encode, key=setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return token


def create_token_email(email_dict: dict):
    to_encode = email_dict.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(hours=int(setting.RESEND_KEY_EXPIRE_TIME))})
    token = jwt.encode(to_encode, key=setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return token


def verify_email_token(token: str):
    payload = jwt.decode(token, key=setting.SECRET_KEY, algorithms=[setting.ALGORITHM], options={'verify_exp': True})
    email: str = payload.get('email')

    if email is None:
        raise InvalidTokenError

    return email
