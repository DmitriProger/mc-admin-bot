import asyncio
import os

from dotenv import load_dotenv

from services.rcon_service import add_to_whitelist

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(add_to_whitelist("Abofsdfsdfby"))

# Запуск: python -m tests.rcon_test
