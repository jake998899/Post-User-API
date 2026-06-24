from fastapi import APIRouter, status, Depends, BackgroundTasks
from database import DB_session
from schemas.pydantic_models import *
from schemas.hashing_file import *
from schemas.crud import *
from schemas.HTTPErrors import *
from schemas.token import *
from models import User
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/signin", status_code=status.HTTP_201_CREATED, response_model=UserReqRes)
async def create_user(db: DB_session, user_req: UserReq):
    try:
        user_exists = await user_exists_service(user_req.username, db)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username alreadt exists",
            )

        email_exists = await fetch_user_email(user_req.email, db)
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="email alreadt exists"
            )

        user_data = user_req.model_dump()
        user_data["password"] = hash_password(user_data["password"])
        user_model = User(**user_data)

        db.add(user_model)
        await db.commit()
        await db.refresh(user_model)
        return user_model

    except HTTPException:
        await db.rollback()
        raise
    except Exception as ex:
        await db.rollback()
        raise ExceptionError(msg=str(ex))


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_user(
    db: DB_session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        user = await user_exists_service(form_data.username, db)
        if not user:
            raise UnAuthorizesError(msg="username or password is incorrect!")

        if not verify_password(form_data.password, user.password):
            raise UnAuthorizesError(msg="username or password is incorrect!")

        token = create_access_token(
            {"sub": user.username, "id": user.id, "role": user.role}
        )
        return {"access_token": token, "token_type": "bearer"}

    except UnAuthorizesError:
        raise
    except Exception as ex:
        raise ExceptionError(msg=str(ex))


@router.get("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    db: DB_session,
    background_tasks: BackgroundTasks,
    email_data: ForgotPasswordEmail = Depends(),
):
    try:
        existing_email = await fetch_user_email(email=email_data.email, db=db)
        if not existing_email:
            raise UnAuthorizesError(msg="Invalid Creadentials")

        email_token = create_token_email({"email": existing_email.email})
        background_tasks.add_task(
            send_email, existing_email.email, email_token, existing_email.username
        )

        return {
            "msg": f"An email has been send to {existing_email.email}. The will expire in 1 hours"
        }

    except UnAuthorizesError:
        raise
    except Exception as ex:
        raise ExceptionError(msg=str(ex))


@router.put(
    "/reset_password", status_code=status.HTTP_200_OK, response_model=UserReqRes
)
async def reset_password(db: DB_session, token: str, reset_req: ResetPasswordReq):
    try:
        email = verify_email_token(token=token)

        user = await fetch_user_email(email=email, db=db)

        if not user:
            raise NotFoundError(msg="Invalid Creadentials")

        user.password = hash_password(reset_req.password)

        await db.commit()
        await db.refresh(user)
        return user
    except NotFoundError:
        await db.rollback()
        raise
    except Exception as ex:
        await db.rollback()
        raise ExceptionError(msg=str(ex))
