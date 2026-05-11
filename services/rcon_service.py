import os

from rcon.source import rcon


async def add_to_whitelist(nickname: str) -> str:
    response = await rcon(
        f"whitelist add {nickname}",
        host=os.getenv("RCON_HOST"),
        port=int(os.getenv("RCON_PORT")),
        passwd=os.getenv("RCON_PASSWORD"),
    )
    print(response)
    return response
