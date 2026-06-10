import logging
import os

from aiogram import Bot
from dotenv import load_dotenv

import app.keyboards as kb
from database.queries import get_topic, save_topic

load_dotenv()
APPLICATIONS_THREAD_ID = int(os.getenv("APPLICATIONS_THREAD_ID"))
ADMIN_CHAT_ID = int(os.getenv("SUPER_GROUP_ID"))


logger = logging.getLogger(__name__)


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


async def send_report(bot: Bot, data, username, user_id, report_id):
    thread_id = await get_or_create_topic(bot, ADMIN_CHAT_ID, user_id, username or str(user_id))
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
                message_thread_id=thread_id,
                photo=first["file_id"],
                caption=text,
                reply_markup=kb.admin_report(report_id),
            )
        elif first["type"] == "video":
            await bot.send_video(
                chat_id=ADMIN_CHAT_ID,
                message_thread_id=thread_id,
                video=first["file_id"],
                caption=text,
                reply_markup=kb.admin_report(report_id),
            )

        for file in files[1:]:
            if file["type"] == "photo":
                await bot.send_photo(
                    chat_id=ADMIN_CHAT_ID,
                    message_thread_id=thread_id,
                    photo=file["file_id"],
                )
            elif file["type"] == "video":
                await bot.send_video(
                    chat_id=ADMIN_CHAT_ID,
                    message_thread_id=thread_id,
                    video=file["file_id"],
                )
    else:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            message_thread_id=thread_id,
            text=text,
            reply_markup=kb.admin_report(report_id),
        )


async def create_topic(bot: Bot, chat_id, user_id, name):
    topic = await bot.create_forum_topic(chat_id=chat_id, name=name)
    await save_topic(user_id, topic.message_thread_id)
    logger.info("Создан топик thread_id=%s для user_id=%s", topic.message_thread_id, user_id)
    return topic.message_thread_id


async def get_or_create_topic(bot: Bot, chat_id, user_id, name):
    thread_id = await get_topic(user_id)
    logger.debug("get_topic для user_id=%s вернул thread_id=%s", user_id, thread_id)

    if thread_id is None:
        thread_id = await create_topic(bot, chat_id, user_id, f"юзер: {name}")

    return thread_id
