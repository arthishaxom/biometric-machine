import asyncio
import logging
import logging.handlers
import os

import motor.motor_asyncio
import config

from typing import List, Optional

import discord
from discord.ext import commands

import jishaku

from utils.buttons import verifyButton

os.environ["JISHAKU_NO_UNDERSCORE"] = "t"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "t"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "t"
os.environ["JISHAKU_HIDE"] = "t"

class KittHive(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        testing_guild_id: Optional[int] = None,
        db_conn,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
        self.db_conn = motor.motor_asyncio.AsyncIOMotorClient(db_conn)

    async def setup_hook(self) -> None:
        await self.load_extension('jishaku')
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)
        
        self.add_view(verifyButton())


async def main():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    exts = ["cogs."+os.path.splitext(file)[0] for file in os.listdir("./cogs") if file.endswith(".py")]
    intents = discord.Intents.default()
    intents.members = True
    async with KittHive(
            commands.when_mentioned,
            initial_extensions=exts,
            intents=intents,
            testing_guild_id=config.GUILD_ID,
            db_conn=config.DB_CONN
        ) as bot:
            await bot.start(config.DISCORD_TOKEN)

asyncio.run(main())
