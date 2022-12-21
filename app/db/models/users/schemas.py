from sqlalchemy import Column, String, DECIMAL, Integer

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    first_name = Column(String(length=64), nullable=False)
    last_name = Column(String(length=64), nullable=False)

    username = Column(String(length=32), unique=True, index=True, nullable=False)
    password = Column(String(length=256), nullable=False)

    balance = Column(DECIMAL(precision=6, scale=2))
