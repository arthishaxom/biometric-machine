import discord
from discord.ext import commands
from discord import app_commands


class Misc(commands.Cog):
    """"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"<a:kh_announce:1261888060103327764> Bot: `{round(self.bot.latency*1000, 2)} ms`"
        )

    @app_commands.command(name="blacklist")
    @app_commands.checks.has_permissions(administrator=True)
    async def blacklist(
        self,
        interaction: discord.Interaction,
        useremail: str = None
    ):
        if(useremail != None):
            db = interaction.client.db_conn.user_info
            veri_details = db["verification_details"]
            result = await veri_details.update_one(
                {"useremail": useremail}, {"$set": {"status": "blacklisted"}}
            )
            await interaction.response.send_message(f"{useremail} is whitelisted!")
        else:
            await interaction.response.send_message("Enter Email Address", ephemeral=True)

    @app_commands.command(name="whitelist")
    @app_commands.checks.has_permissions(administrator=True)
    async def whitelist(
        self,
        interaction: discord.Interaction,
        useremail: str = None
    ):
        if(useremail != None):
            db = interaction.client.db_conn.user_info
            veri_details = db["verification_details"]
            result = await veri_details.update_one(
                {"useremail": useremail}, {"$set": {"status": "verified"}}
            )
            await interaction.response.send_message(f"{useremail} is whitelisted!")
        else:
            await interaction.response.send_message("Enter Email Address", ephemeral=True)

    @app_commands.command(name="remove")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove(
        self,
        interaction: discord.Interaction,
        useremail: str = None
    ):
        if(useremail != None):
            db = interaction.client.db_conn.user_info
            veri_details = db["verification_details"]
            result = await veri_details.delete_one(
                {"useremail": useremail}
            )
            await interaction.response.send_message(f"{useremail} is removed!")
        else:
            await interaction.response.send_message("Enter Email Address", ephemeral=True)



    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error,app_commands.MissingPermissions):
            await interaction.response.send_message("You Don't Have The PERMISSIONS.", ephemeral=True)
            return
            

async def setup(bot):
    await bot.add_cog(Misc(bot))
