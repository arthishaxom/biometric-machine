import functools
import discord
from discord.utils import MISSING
import pyotp
import time
import traceback
import utils.buttons as btn
import utils.funcs as fn
import utils.constants as consts


class emailModal(discord.ui.Modal, title="Type your KIIT mail for OTP"):
    def __init__(self) -> None:
        super().__init__()
        self.email = discord.ui.TextInput(
            label="KIIT Email", placeholder="roll_number@kiit.ac.in", required=True
        )
        self.add_item(self.email)

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        print(traceback.format_exc())
        await interaction.followup.send(
            f"<:kh_error:1261859714304573480> Following error occured : {error}, contact staff",
            ephemeral=True,
        )
        return

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        try:
            if self.email.value.split("@")[1] != "kiit.ac.in":
                await interaction.followup.send(
                    "Enter KIIT Email ID only.", ephemeral=True
                )
                return
        except Exception as e:
            print(e)
            await interaction.followup.send(
                "<:kh_error:1261859714304573480> Enter Valid Email.", ephemeral=True
            )
            return

        db = interaction.client.db_conn.user_info
        veri_details = db["verification_details"]
        result = await veri_details.find_one({"useremail": self.email.value})

        # TODO checking if email already exists
        if result:
            if result["status"] == "verified":
                await interaction.followup.send(
                    "<:kh_error:1261859714304573480> Email is already being used. If not you then contact staff.",
                    ephemeral=True,
                )
                return
            
            # TODO checking if email verified or blacklisted
            elif result["status"] == "blacklisted":
                await interaction.followup.send(
                    "<:kh_error:1261859714304573480> Email is __blacklisted__. If you think it is a mistake then contact staff.",
                    ephemeral=True,
                )
                return

        embed = discord.Embed(
            title="OTP sent to your email",
            description="""Check `SPAM` Folder if not in your `Inbox`.""",
            color=discord.Color.green(),
        )
        embed.set_footer(text="⚠️ OTP is valid for 5 minutes only")

        totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
        currOTP = totp.now()


        await interaction.followup.send(
            embed=embed,
            view=btn.otpButton(totp, self.email.value),
            ephemeral=True,
        )

        thing = functools.partial(fn.sendOtp, self.email.value, currOTP)
        res = await interaction.client.loop.run_in_executor(None, thing)
        if res == "error":
            print(traceback.format_exc())
            await interaction.followup.send(
                "<a:kh_announce:1261888060103327764> Today's quota completed, try again for verification tommorow",
                ephemeral=True,
            )
            return

class otpModal(discord.ui.Modal, title="Enter OTP"):
    def __init__(self, otp, email) -> None:
        super().__init__()
        self.otp = otp
        self.email = email
        self.otpInput = discord.ui.TextInput(
            label="OTP", placeholder="Enter OTP", required=True
        )
        self.add_item(self.otpInput)

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        print(traceback.format_exc())
        return

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        if self.otp.verify(self.otpInput.value):
            year = fn.getInfo(email=self.email)

            try:
                verifiedRole = interaction.guild.get_role(consts.verifiedRole)
                yearRole = interaction.guild.get_role(consts.roleMap[year])

                await interaction.user.add_roles(verifiedRole)
                await interaction.user.add_roles(yearRole)
                db = interaction.client.db_conn.user_info
                veri_details = db["verification_details"]
                await veri_details.insert_one(
                    {
                        "userid": interaction.user.id,
                        "useremail": f"{self.email}",
                        "status": "verified",
                    }
                )
            except Exception as e:
                await interaction.followup.send(
                    f"<:kh_error:1261859714304573480> Error! : {e}, **Contact Staff**",
                    ephemeral=True,
                )
                print(traceback.format_exc())
                return
            await interaction.followup.send(
                f"Verified!! You are given **{yearRole.name}** role", ephemeral=True
            )
            await interaction.message.delete(delay=30)

        else:
            await interaction.followup.send("Invalid", ephemeral=True)
