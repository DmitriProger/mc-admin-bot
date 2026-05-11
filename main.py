import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.register_handlers import register_router
from database.init import init_db


async def main():
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))  # noqa: F841
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.startup.register(start_app)
    dp.shutdown.register(shutdown)
    dp["dp"] = dp
    dp.include_router(register_router)
    await dp.start_polling(bot)


async def start_app(dispatcher: Dispatcher):
    await init_db()


async def shutdown(dispatcher: Dispatcher):
    pass


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
