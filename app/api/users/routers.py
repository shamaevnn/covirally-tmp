from fastapi import APIRouter, Path, Depends

from app.api.auth.utils import get_current_user
from app.api.users.balance import transfer
from app.db.models.users.handlers import create_user
from app.schemas import (
    User,
    CreateUser,
    BalanceResponse,
    TransferBalanceToUser,
    TransferBalanceResponse,
)

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


@users_router.post("/balance/transfer", response_model=TransferBalanceResponse)
async def transfer_user_balance(
    transfer_balance_params: TransferBalanceToUser,
    current_user: User = Depends(get_current_user),
) -> TransferBalanceResponse:
    new_sender_balance, err = await transfer(
        sender=current_user, transfer_params=transfer_balance_params
    )

    if err is not None:
        raise err

    return TransferBalanceResponse(new_balance=new_sender_balance)


@users_router.post("", response_model=User)
async def create_new_user(user_params: CreateUser) -> User:
    return await create_user(create_user_params=user_params)
