import discord
from discord.ext import commands
from typing import Literal, Optional
import importlib

class Sync(commands.Cog):
    """Sync Command"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def reloadUtil(self, ctx):
        try:
            importlib.reload(importlib.import_module('utils.verification'))
            importlib.reload(importlib.import_module('utils'))
            importlib.reload(importlib.import_module('cogs.verify'))

            # Reload the cog
            await self.bot.reload_extension('cogs.verify')

            await ctx.send("Modules and cog reloaded successfully!")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(Sync(bot))