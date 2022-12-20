from decimal import Decimal

from pydantic import BaseModel, Field

from app.config import INIT_BALANCE_FOR_NEW_USER


class User(BaseModel):
    id: int

    first_name: str
    last_name: str
    balance: Decimal


class CreateUser(BaseModel):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    password: str = Field(max_length=32)

    balance: Decimal = Field(decimal_places=2, default=INIT_BALANCE_FOR_NEW_USER)


class BalanceResponse(BaseModel):
    balance: Decimal
