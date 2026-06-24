from fastapi import APIRouter, status
from database import DB_session
from schemas.dependencies import CurrentUser
from schemas.pydantic_models import *


router = APIRouter(prefix='/api/v1/users', tags=['users'])

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserReqRes)
async def me(current_user: CurrentUser):
    return current_user