from typing import Annotated
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from fastapi import Depends
from models import User
from core.database import DB_session
from core.config import setting
from core.security import oauth2_scheme
from core.HTTPErrors import ExceptionError, NotFoundError, UnauthorizedError
from services.crud import user_exists_service


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DB_session
):
    try:
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

    except ExpiredSignatureError:
        raise UnauthorizedError(msg='Token has expired')
    except (InvalidTokenError, DecodeError):
        raise UnauthorizedError(msg='Invalid authentication token')
    except NotFoundError:
        raise
    except Exception as ex:
        raise ExceptionError(msg=str(ex))


CurrentUser = Annotated[User, Depends(get_current_user)]
