from fastapi import HTTPException

from app.schemas import CreateUser


class UserNotFound(HTTPException):
    def __init__(self, user_id: int) -> None:
        super().__init__(status_code=404, detail=f"User {user_id} is not found")


class DatabaseCreateUser(HTTPException):
    def __init__(self, create_params: CreateUser) -> None:
        msg = f"Internal database error while creating user with {create_params=}"
        super().__init__(status_code=500, detail=msg)
