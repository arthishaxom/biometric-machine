import functools
import discord
from discord.utils import MISSING
import pyotp
import time

import utils.buttons as btn
import utils.funcs as fn


class emailModal(discord.ui.Modal, title="Input Your Roll & KIIT Email"):
    roll = discord.ui.TextInput(
        label="Roll Number", placeholder="Enter you roll number", required=True
    )
    email = discord.ui.TextInput(
        label="KIIT Email", placeholder="roll_number@kiit.ac.in", required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if(self.email.value.split("@")[1]!="kiit.ac.in"):
            interaction.response.send_message("Enter KIIT Email ID.")
            return
        
        embed = discord.Embed(
            title="Verify Yourself",
            description="""We have sent a OTP to your KIIT Mail ID, **__CHECK SPAM FOLDER IF NOT IN INBOX__**
                              OTP is valid for **5 minutes** only.
                              Copy the OTP and click the button below to enter OTP & Submit it.""",
            color=discord.Color.blue(),
        )

        totp = pyotp.TOTP(pyotp.random_base32(),interval=300)

        currOTP = totp.now()
        thing = functools.partial(fn.sendOtp,self.email.value,currOTP)
        await interaction.client.loop.run_in_executor(None,thing)

        await interaction.user.send(
            embed=embed,
            view=btn.otpButton(totp,self.email.value)
        )
        await interaction.response.send_message("Check your DM", ephemeral=True)


class otpModal(discord.ui.Modal, title="Enter OTP"):
    def __init__(self, otp, email) -> None:
        super().__init__()
        self.otp = otp
        self.email = email
        self.otpInput = discord.ui.TextInput(label="OTP", placeholder="Enter OTP", required=True)
        self.add_item(self.otpInput)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if(self.otp.verify(self.otpInput.value)):
            year = fn.getInfo(email=self.email)
            roleMap = {
                1 : "1st year",
                2 : "2nd year",
                3 : "3rd year",
                4 : "4th year"
            }
            await interaction.response.send_message("Verified!!")
        else:
            await interaction.response.send_message("Invalid")
