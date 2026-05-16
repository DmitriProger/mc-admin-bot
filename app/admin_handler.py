from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, Message

from app.filters import IsAdmin
from database.queries import approve_user, get_nickname

admin_router = Router()

admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.callback_query(F.data.startswith("accept:"))
async def admin_accept(callback: CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    nickname = await get_nickname(user_id)
    await callback.answer("Принято!")
    await callback.message.edit_text(f"✅ Игрок {nickname} принят!")
