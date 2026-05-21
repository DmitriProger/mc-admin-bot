import os

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from database.queries import get_user_status


class IsNew(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return await get_user_status(event.from_user.id) == "new"


class IsPending(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return await get_user_status(event.from_user.id) == "pending"


class IsApproved(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return await get_user_status(event.from_user.id) == "approved"


class IsNotApproved(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return await get_user_status(event.from_user.id) != "approved"


load_dotenv()
ADMINS = {int(x) for x in os.getenv("ADMINS", "").split(",") if x.strip()}


class IsAdmin(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return event.from_user.id in ADMINS
