from services.crud import user_exists_service, fetch_email_with_id_exclude_service, fetch_username_with_id_exclude_service
from core.database import DB_session
from fastapi import APIRouter, status
from core.dependencies import CurrentUser
from core.HTTPErrors import NotFoundError, ExceptionError, BadRequestError
from schemas.auth import UserReqRes, UserPatchReq, UserPatchRes

router = APIRouter(prefix='/api/v1/users', tags=['users'])

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserReqRes)
async def me(current_user: CurrentUser):
    return current_user

@router.patch('/profile', status_code=status.HTTP_200_OK, response_model=UserPatchRes)
async def edit_profile(db: DB_session, current_user: CurrentUser, user_patch_req: UserPatchReq):
    try:
        user = await user_exists_service(current_user.username, db)
        if user is None:
            raise NotFoundError(msg='User Not Found')
        user_data = user_patch_req.model_dump(exclude_unset=True)

        if 'username' in user_data:
            username_in_db = await fetch_username_with_id_exclude_service(db, current_user.id, user_data['username'])
            if username_in_db:
                raise BadRequestError(msg='Username already exists')
        
        if 'email' in user_data:
            email_in_db = await fetch_email_with_id_exclude_service(db, current_user.id, user_data['email'])
            if email_in_db:
                raise BadRequestError(msg='Email already exists')

        for field, val in user_data.items():
            setattr(user, field, val)

        await db.commit()
        await db.refresh(user)
        return user
    except NotFoundError:
        await db.rollback()
        raise
    except Exception as ex:
        await db.rollback()
        raise ExceptionError(msg=str(ex))
    
@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(db: DB_session, current_user: CurrentUser):
    try:
        user = await user_exists_service(current_user.username, db)
        if user is None:
            raise NotFoundError(msg='User Not Found')
        
        await db.delete(user)
        await db.commit()
    except NotFoundError:
        await db.rollback()
        raise 
    except Exception as ex:
        await db.rollback()
        raise ExceptionError(msg=str(ex))