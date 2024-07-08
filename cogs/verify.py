from discord import app_commands
import discord
from discord.ext import commands
from utils.buttons import verifyButton

class Verify(commands.Cog):
    """verifcation system"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setupchannel")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    async def setupchannel(
        self, interaction: discord.Interaction
    ):
        channel = discord.utils.get(interaction.guild.text_channels, name="verify-yourself")
        if channel:
            await interaction.response.send_message(f"Verfication Channel already exists - <#{channel.id}>")
            return

        channel = await interaction.guild.create_text_channel("verify-yourself")
        embed = discord.Embed(
            title="Verification",
            description="""Click the button below to verify yourself.""",color=discord.Color.from_rgb(255,255,255)
        )
        embed.set_footer(text="Limited to 100 verifications daily. Please be patient if unsuccessful.")
        embed.set_image(url="https://media.discordapp.net/attachments/1254215254695477300/1259758024516435998/standard.gif?ex=668cd896&is=668b8716&hm=f58375b517487cfe29e7aa2ff8f6a017505adc19aeab6bb937d89a8455db987c&=&width=825&height=291")
        await channel.send(embed=embed,view=verifyButton())
        await interaction.response.send_message(f"Verification Channel Created at <#{channel.id}>!")

async def setup(bot):
    await bot.add_cog(Verify(bot))
