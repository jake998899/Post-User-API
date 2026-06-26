from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from sqlalchemy import String, func

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(default='user')
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    password: Mapped[str] = mapped_column(String(250), nullable=False)

    # Make relationship with posts later