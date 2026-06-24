from schemas.token import get_current_user
from fastapi import Depends
from typing import Annotated
from models import User

CurrentUser = Annotated[User, Depends(get_current_user)]
