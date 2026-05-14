import asyncio
import os

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.keyboards as kb
from app.filters import IsApproved, IsNotApproved
from app.states import ApplicationForm

register_router = Router()
register_router.message.filter(IsNotApproved())


@register_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Это бот сервера Valorium — ванильное выживание с RP. Чтобы попасть на сервер, оставь заявку ниже 📝",
        reply_markup=kb.register_keyboard,
    )


@register_router.callback_query(F.data == "submit_application")
async def cmd_submit(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Loading...")
    await state.set_state(ApplicationForm.nickname)
    await callback.message.answer(
        "🎮 Какой у тебя ник в Minecraft? (перепроверь — на него выдадим доступ!)"
    )


@register_router.message(ApplicationForm.nickname)
async def process_nickname(message: Message, state: FSMContext):
    nickname = message.text
    await state.update_data(nickname=nickname)
