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

    await state.set_state(ApplicationForm.age)
    await message.answer("🎂 Сколько тебе лет?")


@register_router.message(ApplicationForm.age)
async def process_age(message: Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)

    await state.set_state(ApplicationForm.experience)
    await message.answer("⛏ Сколько лет играешь в Minecraft?")


@register_router.message(ApplicationForm.experience)
async def process_experience(message: Message, state: FSMContext):
    experience = message.text
    await state.update_data(experience=experience)

    await state.set_state(ApplicationForm.plans)
    await message.answer("🗺 Какие у тебя планы на сервере? Расскажи пару слов")


@register_router.message(ApplicationForm.plans)
async def process_plans(message: Message, state: FSMContext):
    plans = message.text
    await state.update_data(plans=plans)

    await state.set_state(ApplicationForm.rp_situation)
    await message.answer(
        "💎 Игрок оставил незапертый сундук с алмазами в общей зоне. Твои действия?"
    )


@register_router.message(ApplicationForm.rp_situation)
async def process_situation(message: Message, state: FSMContext):
    rp_situation = message.text
    await state.update_data(rp_situation=rp_situation)

    await state.set_state(ApplicationForm.rules)
    await message.answer("Правила сервера\nЗаглушка", reply_markup=kb.rules_keyboard)


@register_router.callback_query(ApplicationForm.rules, F.data == "rules_read")
async def rules_confirmed(callback: CallbackQuery, state: FSMContext):
    await state.update_data(rules=True)
    data = await state.get_data()
    await state.clear()

    await callback.message.edit_text("✅ Заявка отправлена! Ждём решения админов 🎉")
    await callback.answer()
