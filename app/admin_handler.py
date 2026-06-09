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
from app.states import AdminStates
from database.queries import (
    approve_user,
    clear_thread,
    close_report,
    get_nickname,
    get_thread,
    get_user_id_by_topic,
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
async def admin_answer(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ответ игроку:")
    await state.set_state(AdminStates.admin_answer)
    logger.info("Админ %s начал отвечать на тикет", callback.from_user.id)


@admin_router.message(AdminStates.admin_answer)
async def admin_text(message: Message, state: FSMContext, bot: Bot, dp: Dispatcher):
    await state.update_data(admin_answer=message.text)

    admin_text = await state.get_data()
    admin_text = admin_text["admin_answer"]
    thread_id = message.message_thread_id
    user_id = await get_user_id_by_topic(thread_id)
    await bot.send_message(chat_id=user_id, text=admin_text)
    await state.clear()
    logger.info("Админ %s отправил ответ юзеру %s", message.from_user.id, user_id)


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
    logger.info("Админ %s закрыл тикет %s юзера %s", callback.from_user.id, report_id, user_id)


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
