from models import User
from sqlalchemy import select
from database import DB_session
from sqlalchemy.ext.asyncio import AsyncSession


async def user_exists_service(username: str, db: DB_session):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def fetch_user_email(email: str, db: DB_session):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()