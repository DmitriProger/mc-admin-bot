import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.admin_handler import admin_router
from app.register_handlers import register_router
from app.user_handler import user_router
from database.init import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    logger.info("Диспетчер инициализирован")
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp["dp"] = dp
    dp.include_routers(register_router, admin_router, user_router)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    logger.info("Бот запущен")
    await init_db()


async def shutdown(dispatcher: Dispatcher):
    logger.info("Бот выключен")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
