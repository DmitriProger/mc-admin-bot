import os

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from database.queries import user_status


class IsApproved(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await user_status(message.from_user.id)


class IsNotApproved(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not await user_status(message.from_user.id)


load_dotenv()
ADMINS = {int(x) for x in os.getenv("ADMINS", "").split(",") if x.strip()}


class IsAdmin(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return event.from_user.id in ADMINS
