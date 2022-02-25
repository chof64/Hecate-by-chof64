
"""
    ./src/cogs/core/tester.py

    A cog file for testing purposes.
"""

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()


class CoreTester(commands.Cog, name="coretester"):
    """
        Main class for all command functions. This is where the bot
        interacts when a user initiates a command found in this cog.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='testerror', hidden=True)
    @commands.has_any_role(">> L10: DEV <<", ">> SUDO <<")
    async def test_error(self, ctx):
        """
            Command: >>ping
            Roles (any of): >> L9: DEV <<, >> SUDO <<
        """
        raise discord.DiscordException("This is a test error.")


def setup(bot):
    """
        Function that is called when the cog is loaded.
    """
    bot.add_cog(CoreTester(bot))
