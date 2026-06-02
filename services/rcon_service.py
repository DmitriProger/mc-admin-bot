import logging
import os

from rcon.source import rcon

logger = logging.getLogger(__name__)


async def add_to_whitelist(nickname: str) -> str:
    response = await rcon(
        f"whitelist add {nickname}",
        host=os.getenv("RCON_HOST"),
        port=int(os.getenv("RCON_PORT")),
        passwd=os.getenv("RCON_PASSWORD"),
    )
    logger.info("Игрок %s добавлен", nickname)
    print(response)
    return response
