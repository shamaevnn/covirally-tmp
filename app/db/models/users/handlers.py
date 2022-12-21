import logging
from decimal import Decimal
from typing import cast

from pydantic import ValidationError
from sqlalchemy import select, insert, update

from app.api.errors import (
    DatabaseCreateUser,
    UserAlreadyExist,
    InternalErrorTransferBalance,
)
from app.config import INIT_BALANCE_FOR_NEW_USER
from app.db.base import database
from app.db.models.users.schemas import User as UserTable
from app.schemas import User, CreateUser
from app.api.auth.password_utils import get_password_hash

logger = logging.getLogger()


async def get_user(user_id: int) -> User | None:
    query = select(UserTable).where(UserTable.id == user_id).limit(1)
    _res = await database.fetch_one(query)

    if not _res:
        logger.info(f"No user with {user_id=}")
        return None

    try:
        parsed_user: User = User.parse_obj(_res)
    except ValidationError as e:
        logger.error(f"Can't parse {_res}: {e}")
        return None
    else:
        return parsed_user


async def get_user_by_username(username: str) -> User | None:
    query = select(UserTable).where(UserTable.username == username).limit(1)
    _res = await database.fetch_one(query)

    if not _res:
        logger.info(f"No user with {username=}")
        return None

    try:
        parsed_user: User = User.parse_obj(_res)
    except ValidationError as e:
        logger.error(f"Can't parse {_res}: {e}")
        return None
    else:
        return parsed_user


async def create_user(create_user_params: CreateUser) -> User:
    """
    Создаем пользователя, проверяем что пользователь с таким username еще нет.
    Начисляем новым пользователям баланс = INIT_BALANCE_FOR_NEW_USER
    """
    username = create_user_params.username
    already_existing_user = await get_user_by_username(username)
    if already_existing_user is not None:
        raise UserAlreadyExist(username)

    create_user_params.balance = cast(Decimal, INIT_BALANCE_FOR_NEW_USER)
    create_user_params.password = get_password_hash(create_user_params.password)
    create_params = create_user_params.dict()

    query = insert(UserTable).values(**create_params)
    try:
        created_id = await database.execute(query)
    except Exception as e:
        logger.error(
            f"Unexpected error while creating user with {create_user_params=}: {e}"
        )
        raise DatabaseCreateUser(create_params=create_user_params) from e

    user: User = User.construct(**dict(id=created_id, **create_params))
    return user


async def transfer_amount(
    sender: User,
    receiver: User,
    amount: Decimal,
) -> tuple[Decimal | None, Exception | None]:
    transaction = await database.transaction()

    sender_new_balance = sender.balance - amount
    receiver_new_balance = receiver.balance + amount
    try:
        update_sender = (
            update(UserTable)
            .where(UserTable.username == sender.username)
            .values(balance=sender_new_balance)
        )
        update_receiver = (
            update(UserTable)
            .where(UserTable.username == receiver.username)
            .values(balance=receiver_new_balance)
        )

        await database.execute(update_sender)
        await database.execute(update_receiver)

    except Exception as e:
        await transaction.rollback()
        return None, InternalErrorTransferBalance(
            sender_username=sender.username,
            receiver_username=receiver.username,
            amount=amount,
            details=str(e),
        )
    else:
        await transaction.commit()
        return sender_new_balance, None
