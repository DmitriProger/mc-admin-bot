import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from app.filters import IsAdmin
from database.queries import (
    approve_user,
    clear_thread,
    close_report,
    get_nickname,
    get_thread,
    get_user_report,
    reject_user,
)

admin_router = Router()

admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


logger = logging.getLogger(__name__)
load_dotenv()
ADMIN_CHAT_ID = int(os.getenv("SUPER_GROUP_ID"))


@admin_router.callback_query(F.data.startswith("answer:"))
async def admin_answer(callback: CallbackQuery, bot: Bot):
    report_id = int(callback.data.split(":")[1])
    user_id = await get_user_report(report_id)
    # TODO: написать систему ответа на тикет
    await bot.send_message(chat_id=user_id, text="")


@admin_router.callback_query(F.data.startswith("close:"))
async def admin_close(callback: CallbackQuery, bot: Bot):
    report_id = int(callback.data.split(":")[1])
    user_id = await get_user_report(report_id)
    thread_id = await get_thread(user_id)
    await close_report(report_id)
    await bot.delete_forum_topic(chat_id=ADMIN_CHAT_ID, message_thread_id=thread_id)
    await clear_thread(user_id)
    await callback.answer("Тикет закрыт")
    await bot.send_message(chat_id=user_id, text="Админ закрыл тикет")


@admin_router.callback_query(F.data.startswith("accept:"))
async def admin_accept(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split(":")[1])
    nickname = await get_nickname(user_id)
    await approve_user(user_id)

    await callback.answer("Принято!")
    logger.info("Админ %s принял игрока %s", callback.from_user.id, nickname)
    try:
        await callback.message.answer(f"✅ Игрок {nickname} принят!")
    except TelegramBadRequest:
        pass
    await bot.send_message(
        chat_id=user_id,
        text="✅ Поздравляем, вы приняты! Нажмите /start для попадания в главное меню",
    )


@admin_router.callback_query(F.data.startswith("reject:"))
async def admin_reject(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split(":")[1])
    nickname = await get_nickname(user_id)
    await reject_user(user_id)
    await callback.answer("Принято!")
    logger.info("Админ %s отклонил игрока %s", callback.from_user.id, nickname)
    try:
        await callback.message.answer(f"❌ Игрок {nickname} отклонен!")
    except TelegramBadRequest:
        pass

    await bot.send_message(chat_id=user_id, text="❌ К сожалению ваша заявка отклонена")
