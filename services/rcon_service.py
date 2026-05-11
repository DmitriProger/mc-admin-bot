import asyncio

from rcon.source import rcon


async def send_command(ip: str, port: int, password: str, command: str) -> None:
    await rcon(command, host=ip, port=port, passwd=password)
