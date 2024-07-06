import discord
from discord.ext import commands
class Event(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("KIIT Hive is online.")

async def setup(bot):
    await bot.add_cog(Event(bot=bot))