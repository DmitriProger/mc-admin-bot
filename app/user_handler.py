import logging

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.keyboards as kb
from app.filters import IsApproved
from app.states import ReportForm
from database.queries import get_nickname, init_report
from services.topic_service import send_report

user_router = Router()
user_router.message.filter(IsApproved())
user_router.callback_query.filter(IsApproved())

logger = logging.getLogger(__name__)


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    tg_id = message.from_user.id
    nickname = await get_nickname(tg_id)
    await message.answer(
        f"Здравствуйте {nickname}. Вы попали в главное меню, выберите действие",
        reply_markup=kb.user_main,
    )


@user_router.callback_query(F.data == "report")
async def start_report(callback: CallbackQuery, state: FSMContext):
    logger.info("Пользователь %s начал репорт", callback.from_user.id)
    await callback.answer("")
    await state.set_state(ReportForm.nick_offender)
    await callback.message.edit_text("Введите ник нарушителя:", reply_markup=kb.cancel_keyboard)


@user_router.message(ReportForm.nick_offender)
async def nick_offender(message: Message, state: FSMContext):
    nick_offender = message.text
    await state.update_data(nick_offender=nick_offender)
    await state.set_state(ReportForm.violation_type)
    await message.answer("Выберите тип нарушения", reply_markup=kb.report_keyboard)


@user_router.callback_query(ReportForm.violation_type)
async def violation_type(callback: CallbackQuery, state: FSMContext):
    violation_type = callback.data
    if violation_type == "other":
        await state.set_state(ReportForm.custom_violation)
        await callback.message.edit_text(
            "Введите свой тип нарушения:", reply_markup=kb.back_keyboard
        )
    else:
        await state.update_data(violation_type=violation_type)
        await state.set_state(ReportForm.description)
        await callback.message.answer(
            "Введите подробное описание проблемы, координаты, скриншоты, видео"
        )


@user_router.message(ReportForm.custom_violation)
async def custom_violation(message: Message, state: FSMContext):
    violation_type = message.text
    await state.update_data(violation_type=violation_type)
    await state.set_state(ReportForm.description)
    await message.answer("Введите подробное описание проблемы, координаты, скриншоты, видео")


@user_router.message(ReportForm.description)
async def description(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    files = data.get("description_files", [])

    if message.photo:
        files.append({"type": "photo", "file_id": message.photo[-1].file_id})
    elif message.video:
        files.append({"type": "video", "file_id": message.video.file_id})

    await state.update_data(description_files=files, description=message.text)
    data = await state.get_data()

    username = message.from_user.username
    user_id = message.from_user.id

    await send_report(bot, data, username, user_id)
    await init_report(user_id, data["nick_offender"], data["violation_type"], data["description"], status="open")
    await state.clear()
    await message.answer("Репорт отправлен, ожидайте ответа")
    logger.info("Пользователь %s отправил репорт", user_id)


@user_router.message(ReportForm.description)
@user_router.callback_query(F.data == "back")
async def to_violation_type(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(ReportForm.violation_type)
    await callback.message.edit_text("Выберите тип нарушения", reply_markup=kb.report_keyboard)


@user_router.callback_query(F.data == "cancel")
async def to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    tg_id = callback.from_user.id
    nickname = await get_nickname(tg_id)
    await callback.message.edit_text(
        f"Здравствуйте {nickname}. Вы попали в главное меню, выберите действие",
        reply_markup=kb.user_main,
    )
    logger.info("Пользователь %s отменил действие", callback.from_user.id)
