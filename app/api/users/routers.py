from fastapi import APIRouter, Path

from app.api.errors import UserNotFound
from app.db.models.users.handlers import get_user, create_user
from app.schemas import User, CreateUser

users_router = APIRouter(tags=["Users"], prefix="/api/v1/users")


@users_router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int = Path(description="Get user by id")) -> User:
    user = await get_user(user_id=user_id)
    if not user:
        raise UserNotFound(user_id=user_id)
    return user


@users_router.post("", response_model=User)
async def create_new_user(user_params: CreateUser) -> User:
    return await create_user(create_user_params=user_params)