
"""
    ./src/cogs/mastersheet/engine.py

    Engine for the mastersheet. Will be used as the
    backend for the Cataclysm Intelligence Division (CID) Mastersheet.
"""

import json
import os

import aiofiles
import aiohttp
import motor.motor_asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class Helpers():
    """
        Helper functions do the heavy lifting. It is responible for calling
        external data, and processing the data in preparation for the
        Adapters. These functions aim to be reusable and can be used by other
        modules with little to no modification.

        :: stnd_nation_information
        :: cata_bot_discord

        TODO LEARN: Why does Pylint return "R0201: Method could be a function"
                    on these functions.
    """

    @staticmethod
    async def stnd_nation_information(alliance_id):
        """
            Standard Nation Information calls all relevant information of
            all nations in the given alliance from the P&W GraphQL API.

            These information include:
            - Expanded Nation Information
            - Expanded Cities Information
            - Minimum Wars Information (ID, AttackerID, DefenderID)
        """
        # 0.0: Variables.
        json_data_loc = './src/data/cogs/mastersheet.json'
        async with aiofiles.open(json_data_loc, 'r') as file:
            query_data = json.loads(await file.read())
            query_data = query_data['engine']['helpers']
            query_data = query_data['stnd_nation_information']['query_data']
        endpoint = (
            'https://api.politicsandwar.com/graphql'
            f'?api_key={os.getenv("PNW_API_KEY")}'
            )
        query = (
            '{nations(first:2, alliance_id:'+alliance_id+'){'
            'data{'+query_data+'}}}'
        )

        # 0.1: Call the API.
        async with aiohttp.ClientSession() as sessions:
            async with sessions.post(endpoint, json={"query": query}) as resp:
                data = await resp.json()

        # 0.2: Prepare and return the data.
        print(resp)
        print(data)
        return data["data"]["nations"]["data"]

    @staticmethod
    async def cata_bot_discord(nation_id):
        """
            Calls discord user information on specific nation from
            Cata Bot api.

            TODO: Add fallback when API returns an error of "nation not in
                  database." Return null, or something.
        """
        # 0: Variables.
        endpoint = f"https://cotl.pw/api/discord-user/{nation_id}"

        # 1: Call the API
        async with aiohttp.ClientSession() as sessions:
            async with sessions.get(endpoint) as response:
                data = await response.json()

        # 2: Prepare and return the data.
        return data


class Adapters:
    """
        This is the adapters which combine and make Helpers useful.
        This is called by either the commands or running tasks.

        TODO LEARN: Why does Pylint return a "R0201: Method could be a
                    function" on these functions.
    """

    @staticmethod
    async def pull_api_information(alliance_id):
        """
            Adapter: Initiate the pulling of the information needed from
            P&W GraphQl API. This adapter is frequently called as the latest
            information is needed.
        """
        # 0.1: Variables
        using_database = 'mastersheet-engine'
        using_collection = f'{alliance_id}-nations-information'

        # 0.2: Authenticate with the database. (MongoDB)
        db_default = 'main-database'
        db_auth = (
            f'mongodb+srv://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASS")}'
            f'@{os.getenv("DB_URI")}/{db_default}?retryWrites=true&w=majority'
        )
        client = motor.motor_asyncio.AsyncIOMotorClient(db_auth)

        # 1.0: Get Nation Information.
        data = await Helpers.stnd_nation_information(alliance_id)
        # 1.1: Store Nation Information to database.
        db_conn = client[using_database][using_collection]
        for entry in data:
            await db_conn.find_one_and_update(
                {'nation_id': entry['nation_id']},
                {'$set': entry},
                upsert=True
            )

    @staticmethod
    async def pull_cata_bot_discord(alliance_id):
        """
            Adapter: Responsible for pulling discord user information from
            Cata Bot API. This function is called once a day or on demand.
        """
        # 0.0: Variables.
        using_database = 'mastersheet-engine'
        using_collection = f'{alliance_id}-nations-information'

        # 0.1: Authenticate with the database. (MongoDB)
        db_default = 'main-database'
        db_auth = (
            f'mongodb+srv://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASS")}'
            f'@{os.getenv("DB_URI")}/{db_default}?retryWrites=true&w=majority'
        )
        client = motor.motor_asyncio.AsyncIOMotorClient(db_auth)

        # 1.0: Get Nation Information.
        db_conn = client[using_database][using_collection]
        nations = await db_conn.find(
            projection={'nation_id': True}
        ).to_list(length=None)

        # 2.0: Iterate thourgh all alliance nations and call API.
        for one in nations:
            response = await Helpers.cata_bot_discord(one['nation_id'])
            if response.get('error'):
                continue
            # 2.1: Prepare data to be stored to database.
            data = {
                'discord_id': response['id'],
                'username': f'{response["name"]}#{response["discriminator"]}',
                'nickname': response['nick'],
                'name': response['name'],
                'discriminator': response['discriminator'],
                'avatar': response['avatar'],
            }
            # 2.2: Store data to database.
            await db_conn.find_one_and_update(
                {'nation_id': one['nation_id']},
                {'$set': {'user_discord': data}},
                upsert=True
            )


class MastersheetEngine(commands.Cog, name="coreowner"):
    """
        Main class for all command functions. This is what the bot calls
        first when a user uses a command in this cog file.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='msengine', hidden=True)
    @commands.has_any_role(">> SUDO <<", ">> L10 <<", )
    async def ms_engine(self, ctx, alliance_id):
        """
            A command that is responsible for powering the Mastersheet.

            TODO: Breakdown function into sub-functions for easier
                  modifications, etc.
        """
        # 0: Variables.
        bot_latency = round(self.bot.latency * 1000)

        # 1: Call Adapters.
        await Adapters.pull_api_information(alliance_id)
        await Adapters.pull_cata_bot_discord(alliance_id)

        # 3: Response to user command.
        await ctx.send(
            'Mastersheet Engine has been called for ' +
            str(alliance_id) + ' | ' + str(bot_latency)
        )


def setup(bot):
    """
        Function that is called when the cog is loaded.
    """
    bot.add_cog(MastersheetEngine(bot))
