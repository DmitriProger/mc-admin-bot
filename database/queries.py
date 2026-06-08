import logging

import aiosqlite

from database.init import DB_PATH

logger = logging.getLogger(__name__)


async def new_registration(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT OR IGNORE INTO registrations(tg_id) VALUES (?)",
            (tg_id,),
        )
        await conn.commit()
        logger.info("Новая регистрация: %s", tg_id)


async def get_user_status(tg_id) -> str:
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute(
            "SELECT status FROM registrations WHERE tg_id = ?",
            (tg_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "new"
        logger.debug("Получен статус пользователя %s: %s", tg_id, row[0] if row else "new")


async def set_pending(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE registrations SET status = 'pending' WHERE tg_id = ?",
            (tg_id,),
        )
        await conn.commit()
        logger.info("Статус пользователя %s изменён на pending", tg_id)


async def approve_user(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE registrations SET status = 'approved' WHERE tg_id = ?",
            (tg_id,),
        )
        await conn.commit()
        logger.info("Пользователь %s одобрен", tg_id)


async def reject_user(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE registrations SET status = 'rejected' WHERE tg_id = ?",
            (tg_id,),
        )
        await conn.commit()


async def set_nickname(tg_id, nickname):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE registrations SET nickname = ? WHERE tg_id = ?",
            (nickname, tg_id),
        )
        await conn.commit()
        logger.info("Пользователь %s отклонён", tg_id)


async def get_nickname(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute(
            "SELECT nickname FROM registrations WHERE tg_id = ?",
            (tg_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
        logger.debug("Получен ник пользователя %s: %s", tg_id, row[0] if row else None)


async def init_report(tg_id, nick_offender, violation_type, description, status):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "INSERT INTO reports(user_id, nick_offender, violation_type, description, status) VALUES (?, ?, ?, ?, ?)",
            (tg_id, nick_offender, violation_type, description, status),
        )
        await conn.commit()
        return cursor.lastrowid


# TODO: применить эту функцию
async def add_admin_report(admin_tg_id, report_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("UPDATE reports SET admin_id = ? WHERE id = ?", (admin_tg_id, report_id))
        await conn.commit()


async def get_user_report(id):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute(
            "SELECT user_id FROM reports WHERE id = ?",
            (id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def get_thread(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("SELECT topic_id FROM registrations WHERE tg_id = ?", (tg_id,))
        row = await cursor.fetchone()
        return row[0] if row else None


async def save_thread(tg_id, topic_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE registrations SET topic_id = ? WHERE tg_id = ?", (topic_id, tg_id)
        )
        await conn.commit()


async def clear_thread(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("UPDATE registrations SET topic_id = NULL WHERE tg_id = ?", (tg_id,))
        await conn.commit()


async def get_user_id_by_topic(topic_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute(
            "SELECT tg_id FROM registrations WHERE topic_id = ?",
            (topic_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
