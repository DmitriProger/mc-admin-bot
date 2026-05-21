import os

from aiogram import Bot
from dotenv import load_dotenv

import app.keyboards as kb

load_dotenv()
APPLICATIONS_THREAD_ID = int(os.getenv("APPLICATIONS_THREAD_ID"))
ADMIN_CHAT_ID = int(os.getenv("SUPER_GROUP_ID"))


async def send_to_topic(bot: Bot, data, username, user_id):
    text = f"""╭─ 📩 Новая заявка ─╮

👤 @{username} ({user_id})

🎮 Ник: {data["nickname"]}
🎂 Возраст: {data["age"]}
⛏ Стаж: {data["experience"]}

🗺 Планы на сервере:
└ {data["plans"]}

💎 Сундук с алмазами:
└ {data["rp_situation"]}

📜 Правила прочитаны ✅"""

    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        message_thread_id=APPLICATIONS_THREAD_ID,
        text=text,
        reply_markup=kb.admin_keyboard(user_id),
    )
