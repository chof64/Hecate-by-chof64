
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
    async def test_error(self, ctx, verify):
        """
            Command: >>ping
            Roles (any of): >> L9: DEV <<, >> SUDO <<
        """
        # 0: Variables
        verify = verify.lower()

        # 1: Checking and execution
        if verify != "verify":
            example = ">>testerror verify"
            latency = round(self.bot.latency * 1000)
            await ctx.send(f'You need to type "verify" to execute command. `{example}` | {latency}')
        else:
            raise discord.DiscordException("This is a test error.")


def setup(bot):
    """
        Function that is called when the cog is loaded.
    """
    bot.add_cog(CoreTester(bot))
