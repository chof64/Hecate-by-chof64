"""
./core/status.py
"""

from discord.ext import commands


class Status(commands.Cog, name="Core: Status"):
    """
    Core: Status

    Contains all commands relating to bot status and uptime.

    There is also a planned group of commands that will be adde
    at a later date to monitor database and system resources and usage.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Ping command.
        """
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")


async def setup(bot):
    """
    Setup function.
    """
    await bot.add_cog(Status(bot))
