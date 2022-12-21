from decimal import Decimal

from pydantic import BaseModel, Field, validator, ValidationError


class User(BaseModel):
    id: int

    first_name: str
    last_name: str

    username: str
    password: str

    balance: Decimal


class CreateUser(BaseModel):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)

    username: str = Field(max_length=32)
    password: str = Field(max_length=32)

    balance: Decimal = Field(decimal_places=2, default=0.0, repr=False)


class BalanceResponse(BaseModel):
    balance: Decimal


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TransferBalanceToUser(BaseModel):
    transfer_amount: Decimal
    receiver_username: str

    @validator("transfer_amount")
    def amount_gt_0(cls, amount: Decimal) -> Decimal:
        assert amount > 0, "Transfer amount must be positive"
        return amount

    def validate_params(self, sender: User) -> None:
        if sender.balance < self.transfer_amount:
            msg = (
                f"Transfer amount is greater than sender balance,"
                f" balance={sender.balance} and amount={self.transfer_amount}"
            )
            raise ValueError(msg)


class TransferBalanceResponse(BaseModel):
    new_balance: Decimal
