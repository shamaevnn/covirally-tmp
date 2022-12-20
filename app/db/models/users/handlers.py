import logging

from pydantic import ValidationError
from sqlalchemy import select, insert

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


async def create_user(create_user_params: CreateUser) -> None:
    query = insert(UserTable).values(**create_user_params.dict())
    await database.execute(query)
