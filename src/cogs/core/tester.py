"""
    ./src/cogs/core/tester.py

    A cog file for testing purposes.
"""

import discord
from discord.ext import commands
from dotenv import load_dotenv

from components.responses import GenericResponse

load_dotenv()


class CoreTester(commands.Cog, name="coretester"):
    """
        Main class for all command functions. This is where the bot
        interacts when a user initiates a command found in this cog.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='testerror', hidden=True)
    @commands.has_any_role(">> SUDO <<")
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
            await ctx.send(f'''You need to type "verify" to execute command.
             `E.g: {example}` | {latency}''')
        else:
            raise discord.DiscordException("This is a test error.")

    @commands.command(name="testroles", hidden=True)
    @commands.has_any_role(">> NO_ROLE <<")
    async def test_roles(self, ctx, *,message):
        """
            Command: >>testroles
            Roles (any of): >> NO_ROLE <<
        """
        await ctx.send(message)

    @commands.command(name="testembed", hidden=True)
    @commands.has_any_role(">> SUDO <<")
    async def test_embed(self, ctx,*, message):
        await GenericResponse.resp_successful(self, ctx, title="Successful Execution", description=message)

def setup(bot):
    """
        Function that is called when the cog is loaded.
    """
    bot.add_cog(CoreTester(bot))
