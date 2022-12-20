from decimal import Decimal

from pydantic import BaseModel

from app.config import INIT_BALANCE_FOR_NEW_USER


class User(BaseModel):
    id: int

    first_name: str
    last_name: str
    balance: float


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    balance: Decimal = Decimal(INIT_BALANCE_FOR_NEW_USER)
