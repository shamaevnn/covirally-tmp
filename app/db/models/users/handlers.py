import logging

from pydantic import ValidationError
from sqlalchemy import select, insert

from app.api.errors import DatabaseCreateUser
from app.db.base import database
from app.db.models.users.schemas import User as UserTable
from app.schemas import User, CreateUser


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


async def create_user(create_user_params: CreateUser) -> User:
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
