from fastapi import HTTPException

from app.schemas import CreateUser


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
