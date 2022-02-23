
"""
    ./src/cogs/mastersheet/engine.py

    Engine for the mastersheet. Will be used as the
    backend for the Cataclysm Intelligence Division (CID) Mastersheet.
"""

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
import discord
import aiohttp
import os


load_dotenv()


class Helpers():
    """
        Helper functions, a breakdown of Adapter functions.
        Do most of the heavy lifting.
    """


    async def pnw_graphql():
        """
            Get the PNW GraphQL endpoint.
        """
        # 0: Variables
        api_key = os.getenv('PNW_API_KEY')
        api_url = f'https://api.politicsandwar.com/graphql?api_key={api_key}'
        payload = None

        async with aiohttp.ClientSession() as session:
            async with session.post(url=api_url, json={'query': payload}) as resp:
                resp.status



class Adapters():
    """
        Adapter functions combining multiple helper functions
        to make command functions more modular and easy to maintain
        and debug.

        ENGINE BREAKDOWN
            01: Pull configuration information from `CID: MS-Engine Configuration`,
                sanitize and format information, and store it locally. (Optional)
            02: Pull all datasets needed (P&W GraphQL APIs, Cata Bot Discord User Information, etc.)
                and store it on MongoDB.
            03: Combine information from datasets into one set that is ready to be pushed.
            04: Push information to google sheets, every x time or on demand.
    """


    # 02
    async def pull_api_information():
        """
            Pulls information from the P&W GraphQL APIs and stores it in MongoDB.

            API TO PULL:
                01.1: P&W GraphQL API Information (update every x time or on demand)
                01.2: Cata Bot Discord User Information (updates every week, or if don't exist)
        """
        


    # 03
    async def combine_api_information():
        """
            Combines information from the P&W GraphQL APIs and Discord User information
            into one set that is ready to be pushed to google sheets.
        """
        

    # 04
    async def push_information():
        """
            Pushes information to google sheets.
        """
        



class MastersheetEngine(commands.Cog, name="coreowner"):
    """
        Main class for all command functions. This is where the bot
        interacts when a user initiates a command found in this cog.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='msengine', hidden=True)
    @commands.has_any_role(">> SUDO <<", ">> L10 <<", )
    async def ms_engine(self, ctx):
        """
            A command that is responsible for powering the Mastersheet.

            TODO: Breakdown function into sub-functions for easier modifications, etc.
        """



def setup(bot):
    """
        Function that is called when the cog is loaded.
    """
    bot.add_cog(MastersheetEngine(bot))
