from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.api.errors import InvalidCredentials, UserNotFound
from app.api.auth.password_utils import password_is_correct
from app.db.models.users.handlers import get_user_by_username
from app.schemas import User
from app.types import JWTData

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def authenticate_user(username: str, password: str) -> User | None:
    user = await get_user_by_username(username)
    if not user:
        return None
    if not password_is_correct(password, user.password):
        return None
    return user


def create_access_token(
    data: JWTData, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)  # type: ignore # noqa
    token: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload: JWTData = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("username")
        if username is None:
            raise InvalidCredentials
    except JWTError as e:
        raise InvalidCredentials from e
    user = await get_user_by_username(username=username)
    if user is None:
        raise UserNotFound(user_param=username)
    return user
