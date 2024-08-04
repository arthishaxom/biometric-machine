import discord
import utils.modals as md

class verifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green,custom_id="verifyView:verfyBtn")
    async def verifyBtn(self, interaction: discord.Interaction, button: discord.Button):
        modal = md.emailModal()
        await interaction.response.send_modal(modal)


class otpButton(discord.ui.View):
    def __init__(self, otp, email: str, timeout: float | None = 300):
        self.otp=otp
        self.email = email
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="Enter OTP", style=discord.ButtonStyle.green)
    async def otpBtn(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(md.otpModal(self.otp,self.email))