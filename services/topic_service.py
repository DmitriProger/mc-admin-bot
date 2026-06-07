import os

from aiogram import Bot
from dotenv import load_dotenv

import app.keyboards as kb

load_dotenv()
APPLICATIONS_THREAD_ID = int(os.getenv("APPLICATIONS_THREAD_ID"))
REPORT_THREAD_ID = int(os.getenv("REPORT_THREAD_ID"))
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
        reply_markup=kb.admin_app(user_id),
    )


async def send_report(bot: Bot, data, username, user_id):
    text = f"""╭─ 🚨 Новый репорт ─╮

👤 От: @{username} ({user_id})

🎮 Ник нарушителя: {data["nick_offender"]}
⚠️ Тип нарушения: {data["violation_type"]}

📝 Описание:
└ {data["description"]}"""

    files = data.get("description_files", [])

    if files:
        first = files[0]
        if first["type"] == "photo":
            await bot.send_photo(
                chat_id=ADMIN_CHAT_ID,
                message_thread_id=REPORT_THREAD_ID,
                photo=first["file_id"],
                caption=text,
                reply_markup=kb.admin_report(user_id),
            )
        elif first["type"] == "video":
            await bot.send_video(
                chat_id=ADMIN_CHAT_ID,
                message_thread_id=REPORT_THREAD_ID,
                video=first["file_id"],
                caption=text,
                reply_markup=kb.admin_report(user_id),
            )

        for file in files[1:]:
            if file["type"] == "photo":
                await bot.send_photo(
                    chat_id=ADMIN_CHAT_ID, message_thread_id=REPORT_THREAD_ID, photo=file["file_id"]
                )
            elif file["type"] == "video":
                await bot.send_video(
                    chat_id=ADMIN_CHAT_ID, message_thread_id=REPORT_THREAD_ID, video=file["file_id"]
                )
    else:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            message_thread_id=REPORT_THREAD_ID,
            text=text,
            reply_markup=kb.admin_report(user_id),
        )
