
"""
    CataScroll Mastersheet (CSM) Cog.

    Responsible for powering CataScroll: Mastersheet.
"""

from discord.ext import commands
import aiohttp
import motor.motor_asyncio


class CataScrollMastersheetEngine():

    async def csme_payload(type):
        """
            Responsible for loadng the right payload for the API call.

            Parameters:
            -   type (str): what type of operation to use. Defaults to get.
            -   identifier (str): identifier of the payload to get, this
                    depends on the function and purpose.
        """
        


    async def csme_pull():



class CataScrollMastersheet(commands.Cog, name="CataScroll Mastersheet (CSM)"):
    """
        Main class of the file. Will contain all commands of the category
        that users can run.
    """

    @commands.command(name='csm_info', hidden=True)
    async def csm_info(self, ctx):
        """
            Command that returns information about the Catascroll Mastersheet
            command category.

            TODO: Add more information about the category.
            TODO: Format response message to be returned by the category.
            TODO: Rewrite message to be more informative.
        """
        await ctx.send(
            "This is a placeholder message to be written and updated in the"
            "future."
        )

    @commands.command(name='csm_engine', hidden=True)
    async def csm_engine(self,ctx)
        """
            The CataScroll: Mastersheet engine.
        """


def setup(bot):
    """
        Function that will load the cog into the bot to be used.
    """
    bot.add_cog(CataScrollMastersheet(bot))
