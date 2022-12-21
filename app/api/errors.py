from decimal import Decimal

from fastapi import HTTPException

from app.schemas import CreateUser, TransferBalanceToUser


class UserNotFound(HTTPException):
    def __init__(self, user_param: int | str) -> None:
        super().__init__(status_code=404, detail=f"User {user_param} is not found")


class DatabaseCreateUser(HTTPException):
    def __init__(self, create_params: CreateUser) -> None:
        msg = f"Internal database error while creating user with {create_params=}"
        super().__init__(status_code=500, detail=msg)


class UserAlreadyExist(HTTPException):
    def __init__(self, username: str) -> None:
        msg = f"User with {username=} already exists."
        super().__init__(status_code=400, detail=msg)


class InvalidCredentials(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Invalid credentials")


class BadRequestTransferBalance(HTTPException):
    def __init__(self, params: TransferBalanceToUser, details: str) -> None:
        super().__init__(status_code=400, detail=f"Invalid {params=}, details: {details}")


class InternalErrorTransferBalance(HTTPException):
    def __init__(
        self, sender_username: str, receiver_username: str, amount: Decimal, details: str
    ) -> None:
        msg = f"Couldn't send {amount=} from {sender_username} to {receiver_username}, details: {details}"  # noqa
        super().__init__(status_code=500, detail=msg)
