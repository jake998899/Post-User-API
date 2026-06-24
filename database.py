from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import setting
from fastapi import Depends
from typing import Annotated

engine = create_async_engine(setting.url, echo=True, future=True)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as sesstion:
        yield sesstion

DB_session = Annotated[AsyncSession, Depends(get_db)]
