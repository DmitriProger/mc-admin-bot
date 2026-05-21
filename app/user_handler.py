from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.keyboards as kb
from app.filters import IsApproved

user_router = Router()
user_router.message.filter(IsApproved())
user_router.callback_query.filter(IsApproved())


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Ты попал в меню бота сервера Valorium, \n пока-что тут пусто ;)")
