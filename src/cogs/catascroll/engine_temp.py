
"""
    A temporary cog that will pull nations information from API and put it
    into MongoDB before outputting it to the CataScroll: Mastersheet.
"""

from discord.ext import commands
import aiohttp
import motor.motor_asyncio

class CataScrollNations(commands.Cog, name=("CataScroll Mastersheet - "
"Nations (CSM-N)")):
    """
        TODO
        - Add a `start`, `stop`, `restart` function for the engine
        - Add a `status` function to check if the engine is running or not
    """

    def __init__(self, bot):
        self.bot = bot


    # @commands.command(name="csengine")
    # async def cs_engine(self, ctx):
    #     """
    #         This command is used for interacting with CataScroll Engine backend.
    #     """
    #     await ctx.send("csengine: under development.")

    @commands.command(name='nations', aliases=["csnhelp","csninfo"],
    hidden=True)
    async def csn_info(self, ctx):
        """
            This function will be the help command for the nations command.
        """
        await ctx.send(
            "These commands are responsible for temporarily running "
            "CataScroll: Mastersheet. The engine will pull all relevant "
            "information from P&W GraphQL API and store it in the bot's "
            "database before outputting it to the mastersheet. \n"
            "If you have any questions, or found any bugs, please contact "
            f"the bot's developer, <@!{self.bot.owner_id}>."
        )


    async def engine_start(self, ctx):
        """
            This command will start the engine.
        """

        await ctx.send("Starting the engine...")




def setup(bot):
    """
        Function that will load the cog into the bot to be used.
    """
    bot.add_cog(CataScrollNations(bot))
