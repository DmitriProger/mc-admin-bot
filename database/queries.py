import aiosqlite

from database.init import DB_PATH


async def new_registration(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT OR IGNORE INTO registrations(tg_id) VALUES (?)",
            (tg_id,),
        )

        await conn.commit()


async def approve_user(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE registrations SET is_approved = TRUE WHERE tg_id = ?",
            (tg_id,),
        )
        await conn.commit()


async def user_status(tg_id):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "SELECT is_approved FROM registrations WHERE tg_id = ?",
            (tg_id,),
        )
        row = await cursor.fetchone()
        return bool(row and row[0])
