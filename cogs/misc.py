import discord
from discord.ext import commands
from discord import app_commands
class Misc(commands.Cog):
    """"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping")
    async def ping(self,interaction: discord.Interaction):
        await interaction.response.send_message(f"<a:kh_announce:1261888060103327764> Bot: `{round(self.bot.latency*1000, 2)} ms`")

async def setup(bot):
    await bot.add_cog(Misc(bot))