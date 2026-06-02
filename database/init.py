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
        await conn.commit()
        logger.info("База данных инициализирована")
