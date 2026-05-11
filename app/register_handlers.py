import asyncio
import os

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.filters import IsApproved, IsNotApproved
import app.keyboards as kb

register_router = Router()
register_router.message.filter(IsNotApproved())


@register_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=kb.register_keyboard)
