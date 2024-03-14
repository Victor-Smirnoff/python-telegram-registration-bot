from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=128), nullable=False)
