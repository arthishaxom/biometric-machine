import functools
import discord
from discord.utils import MISSING
import pyotp
import time

import utils.buttons as btn
import utils.funcs as fn


class emailModal(discord.ui.Modal, title="Input Your Roll & KIIT Email"):
    def __init__(self) -> None:
        super().__init__()
        self.email = discord.ui.TextInput(
            label="KIIT Email", placeholder="roll_number@kiit.ac.in", required=True
        )
        self.add_item(self.email)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if self.email.value.split("@")[1] != "kiit.ac.in":
            await interaction.response.send_message("Enter KIIT Email ID only.",ephemeral=True)
            return

        embed = discord.Embed(
            title="Verify Yourself",
            description="""We have sent a OTP to your KIIT Mail ID, \n**__CHECK SPAM FOLDER IF NOT IN INBOX__**\nOTP is valid for **5 minutes** only, Click the button below to get verified.""",
            color=discord.Color.blue(),
        )

        totp = pyotp.TOTP(pyotp.random_base32(), interval=300)

        currOTP = totp.now()
        thing = functools.partial(fn.sendOtp, self.email.value, currOTP)
        res = await interaction.client.loop.run_in_executor(None, thing)
        if(res == "error"):
            await interaction.response.send_message("We Have Crossed the limit of 100 verifications, kindly try again tomorrow.",ephemeral=True)
            return

        guild = interaction.guild
        userId = interaction.user.id

        await interaction.user.send(
            embed=embed, view=btn.otpButton(totp, self.email.value, guild, userId)
        )
        await interaction.response.send_message("Check your DM", ephemeral=True)


class otpModal(discord.ui.Modal, title="Enter OTP"):
    def __init__(self, otp, email, guild: discord.Guild, userId) -> None:
        super().__init__()
        self.otp = otp
        self.email = email
        self.guild = guild
        self.userId = userId
        self.otpInput = discord.ui.TextInput(
            label="OTP", placeholder="Enter OTP", required=True
        )
        self.add_item(self.otpInput)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if self.otp.verify(self.otpInput.value):
            year = fn.getInfo(email=self.email)
            roleMap = {1: "1st year", 2: "2nd year", 3: "3rd year", 4: "4th year"}
            verifiedRole = discord.utils.get(self.guild.roles, name="verified")
            yearRole = discord.utils.get(self.guild.roles, name=roleMap[year])
            await self.guild.get_member(self.userId).add_roles(verifiedRole)
            await self.guild.get_member(self.userId).add_roles(yearRole)
            await interaction.response.send_message(
                f"Verified!! You are given **{roleMap[year]}** role",delete_after=30
            )
            await interaction.message.delete(delay=30)

        else:
            await interaction.response.send_message("Invalid",delete_after=30)
