from decimal import Decimal

from pydantic import ValidationError

from app.api.errors import UserNotFound, BadRequestTransferBalance
from app.db.models.users.handlers import get_user_by_username, transfer_amount
from app.schemas import TransferBalanceToUser, User


async def transfer(
    sender: User, transfer_params: TransferBalanceToUser
) -> tuple[Decimal | None, Exception | None]:
    """
    Списывает баланс у sender, добавляет к receive_user.
    Возвращается кортеж, первое значение -- новый баланс sender, второе значение -- опциональная ошибка  # noqa
    """
    receiver = await get_user_by_username(username=transfer_params.receiver_username)
    if receiver is None:
        return None, UserNotFound(user_param=transfer_params.receiver_username)

    try:
        transfer_params.validate_params(sender=sender)
    except (ValidationError, ValueError) as e:
        return None, BadRequestTransferBalance(params=transfer_params, details=str(e))

    return await transfer_amount(
        sender=sender, receiver=receiver, amount=transfer_params.transfer_amount
    )
