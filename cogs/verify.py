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
        embed = discord.Embed(
            title="Verification",
            description="""Click the button below, then enter the KIIT mail & OTP""",color=discord.Color.from_rgb(255,255,255)
        )
        embed.set_footer(text="Limited to 100 verifications daily. Please be patient if unsuccessful.")
        embed.set_image(url="https://media.discordapp.net/attachments/1028362108884226069/1259904743099203695/standard.gif?ex=668d613a&is=668c0fba&hm=21c8a7f28a5177155b6842b73338e6c14663e42ff2fe0d1602935cb58d3ceef5&")
        if channel:
            await interaction.response.send_message(f"Verfication Channel already exists - <#{channel.id}>")
            async for msg in channel.history(limit=5):
                if msg.author == self.bot.user:
                    await msg.edit(embed=embed,view=verifyButton())
                    return
            await channel.send(embed=embed,view=verifyButton())
            return
        else:
            channel = await interaction.guild.create_text_channel("verify-yourself")
            await channel.send(embed=embed,view=verifyButton())
            await interaction.response.send_message(f"Verification Channel Created at <#{channel.id}>!")

async def setup(bot):
    await bot.add_cog(Verify(bot))
