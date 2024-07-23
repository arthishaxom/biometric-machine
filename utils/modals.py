import functools
import discord
from discord.utils import MISSING
import pyotp
import time
import traceback
import utils.buttons as btn
import utils.funcs as fn


class emailModal(discord.ui.Modal, title="Type your KIIT mail for OTP"):
    def __init__(self) -> None:
        super().__init__()
        self.email = discord.ui.TextInput(
            label="KIIT Email", placeholder="roll_number@kiit.ac.in", required=True
        )
        self.add_item(self.email)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        print(traceback.format_exc())
        await interaction.followup.send(f"<:kh_error:1261859714304573480> Following error occured : {error}, contact staff",ephemeral=True)
        return

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        try:
            if self.email.value.split("@")[1] != "kiit.ac.in":
                await interaction.followup.send("Enter KIIT Email ID only.",ephemeral=True)
                return
        except Exception as e:
            print(e)
            await interaction.followup.send("<:kh_error:1261859714304573480> Enter Valid Email.", ephemeral=True)
            return

        embed = discord.Embed(
            title="OTP sent to your email",
            description="""Check `SPAM` Folder if not in your `Inbox`.""",
            color=discord.Color.green(),
        )
        embed.set_footer(text="⚠️ OTP is valid for 5 minutes only")
        
        guild = interaction.guild
        userId = interaction.user.id
        totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
        currOTP = totp.now()

        await interaction.user.send(
            embed=embed, view=btn.otpButton(totp, self.email.value, guild, userId)
        )

        thing = functools.partial(fn.sendOtp, self.email.value, currOTP)
        res = await interaction.client.loop.run_in_executor(None, thing)
        if(res == "error"):
            print(traceback.format_exc())
            await interaction.followup.send("<a:kh_announce:1261888060103327764> Today's quota completed, try again for verification tommorow",ephemeral=True)
            return

        await interaction.followup.send("Check your DM", ephemeral=True)


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

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        print(traceback.format_exc())
        return

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if self.otp.verify(self.otpInput.value):
            year = fn.getInfo(email=self.email)
            roleMap = {1: "1st year", 2: "2nd year", 3: "3rd year", 4: "4th year"}
            try:
                verifiedRole = discord.utils.get(self.guild.roles, name="Lovable KIITian")
                yearRole = discord.utils.get(self.guild.roles, name=roleMap[year])
                await self.guild.get_member(self.userId).add_roles(verifiedRole)
                await self.guild.get_member(self.userId).add_roles(yearRole)
            except Exception as e:
                print(traceback.format_exc())
            await interaction.followup.send(
                f"Verified!! You are given **{roleMap[year]}** role",ephemeral=True
            )
            await interaction.message.delete(delay=30)

        else:
            await interaction.followup.send("Invalid",ephemeral=True)
