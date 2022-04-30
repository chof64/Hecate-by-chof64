
"""
    ./src/cogs/core/ping.py

    A cog file specifically for the ping command. And for future
    commands specific to bot network performance.
"""

from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class CorePing(commands.Cog, name="coreping"):
    """
        Main class for all command functions. This is where the bot
        interacts when a user initiates a command found in this cog.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', hidden=True)
    @commands.has_any_role(">> SUDO <<")
    async def hecate_ping(self, ctx):
        """
            A command that returns the bot's latency.

            Command: >>ping
            Roles (any of): >> L9: DEV <<, >> SUDO <<
        """
        # 0: Embed Information (Title, Description, Color)
        embed = discord.Embed(
            title="Hecate is online!",
            description="Hecate is up and always watching.",
            color=0xFBFBFF
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        command_path = ctx.command.qualified_name
        bot_latency = round(self.bot.latency * 1000)
        embed.set_footer(text=f'{command_path}  |  {bot_latency}')
        embed.timestamp = datetime.utcnow()
        # 1: Send the embed to the channel when command is inititated.
        await ctx.send(embed=embed)


def setup(bot):
    """
        Function that is called when the cog is loaded.
    """
    bot.add_cog(CorePing(bot))
