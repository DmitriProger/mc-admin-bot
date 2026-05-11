import aiosqlite

DB_PATH = "data.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""CREATE TABLE IF NOT EXISTS registrations (
                tg_id INTEGER PRIMARY KEY,
                is_approved BOOLEAN DEFAULT FALSE
            )                  
        """)
        await conn.commit()
