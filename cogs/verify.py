from discord import app_commands
import discord
from discord.ext import commands
from utils.buttons import verifyButton

class Verify(commands.Cog):
    """verifcation system"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def setchannel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        embed = discord.Embed(
            title="Verify Yourself",
            description="""
            Click the button below to verify yourself
            > You will get a DM from the bot.""",color=discord.Color.blue()
        )
        await channel.send(embed=embed,view=verifyButton())
        await interaction.response.send_message("Sent!")


async def setup(bot):
    await bot.add_cog(Verify(bot))
