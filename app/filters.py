from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.queries import user_status


class IsApproved(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await user_status(message.from_user.id)


class IsNotApproved(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not await user_status(message.from_user.id)
