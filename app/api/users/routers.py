from fastapi import APIRouter, Path, Depends

from app.api.auth.utils import get_current_user
from app.db.models.users.handlers import create_user
from app.schemas import User, CreateUser, BalanceResponse

users_router = APIRouter(tags=["Users"], prefix="/users")


@users_router.get("/me", response_model=User)
async def get_user_info_for_logged_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user


@users_router.get("/balance", response_model=BalanceResponse)
async def get_user_balance(
    current_user: User = Depends(get_current_user),
) -> BalanceResponse:
    return BalanceResponse(balance=current_user.balance)


@users_router.post("", response_model=User)
async def create_new_user(user_params: CreateUser) -> User:
    return await create_user(create_user_params=user_params)
