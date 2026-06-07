import logging

import aiosqlite

DB_PATH = "data.db"


logger = logging.getLogger(__name__)


async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""CREATE TABLE IF NOT EXISTS registrations (
                tg_id INTEGER PRIMARY KEY,
                status TEXT DEFAULT 'new',
                nickname TEXT UNIQUE
            )
        """)
        logger.info("Таблица registrations инициализирована")

        await conn.execute("""CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                nick_offender TEXT,
                violation_type TEXT,
                description TEXT,
                status TEXT DEFAULT 'open',
                admin_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        logger.info("Таблица reports инициализирована")
        await conn.commit()
        logger.info("База данных инициализирована")
