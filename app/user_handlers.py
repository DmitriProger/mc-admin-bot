import asyncio
import os

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!")
