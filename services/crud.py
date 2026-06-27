from models import User
from sqlalchemy import select
from core.database import DB_session


async def user_exists_service(username: str, db: DB_session):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def fetch_user_email(email: str, db: DB_session):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def fetch_username_with_id_exclude_service(db: DB_session, id: int, username: str):
    result = await db.execute(select(User).where(User.username == username, User.id != id))
    return result.scalar_one_or_none()

async def fetch_email_with_id_exclude_service(db: DB_session, id: int, email: str):
    result = await db.execute(select(User).where(User.email == email, User.id != id))
    return result.scalar_one_or_none()

