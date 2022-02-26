
"""
    ./src/cogs/mastersheet/engine.py

    Engine for the mastersheet. Will be used as the
    backend for the Cataclysm Intelligence Division (CID) Mastersheet.
"""

import os
# from datetime import datetime

import aiohttp
# import discord
import motor.motor_asyncio
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()


class Helpers():
    """
        Helper functions do the heavy lifting. It is responible for calling external data,
        and processing the data in preparation for the Adapters.
        These functions aim to be reusable and can be used by other modules with
        little to no modification.

        :: stnd_nation_information
        :: cata_bot_discord

        TODO LEARN: Why does Pylint return a "R0201: Method could be a function"
                    on these functions.
    """
    @staticmethod
    async def stnd_nation_information(alliance_id):
        """
            Standard Nation Information calls all relevant information of all nations
            in the given alliance from the P&W GraphQL API.

            These information include:
            - Expanded Nation Information
            - Expanded Cities Information
            - Minimum Wars Information (ID, AttackerID, DefenderID)
        """
        # 0.0: Variables.
        endpoint_url = f"https://api.politicsandwar.com/graphql?api_key={os.getenv('PNW_API_KEY')}"
        query = """{
  nations(first:2,alliance_id:"""+alliance_id+"""){
    data{
      nation_id: id,
			alliance_id,
      alliance_position,
      nation_name,
      leader_name,
      continent,
      warpolicy,
      dompolicy,
      color
      num_cities,
      cities{
        id,
        nation_id,
        name,
        date,
        infrastructure,
        land,
        powered,
        oilpower,
        windpower,
        coalpower,
        nuclearpower,
        coalmine,
        oilwell,
        uramine,
        barracks,
        farm,
        policestation,
        hospital,
        recyclingcenter,
        subway,
        supermarket,
        bank,
        mall,
        stadium,
        leadmine,
        ironmine,
        bauxitemine,
        gasrefinery,
        aluminumrefinery,
        steelmill,
        munitionsfactory,
        factory,
        airforcebase,
        drydock,
        nukedate
      },
      score,
      update_tz,
      population,
      flag,
      vmode,
      beigeturns,
      espionage_available,
      last_active,
      date,
      soldiers,
      tanks,
      aircraft,
      ships,
      missiles,
      nukes,
      spies,
      nation_discord: discord,
      wars{
        id,
        attid,
        defid
      }
      turns_since_last_city,
      turns_since_last_project,
      money,
      coal,
      oil,
      uranium,
      iron,
      bauxite,
      lead,
      gasoline,
      munitions,
      steel,
      aluminum,
      food,
      projects,
      project_bits,
      ironw,
      bauxitew,
      armss,
      egr,
      massirr,
      itc,
      mlp,
      nrf,
      irond,
      vds,
      cia,
      cfce,
      propb,
      uap,
      city_planning,
      adv_city_planning,
      space_program,
      spy_satellite,
      moon_landing,
      pirate_economy,
      recycling_initiative,
      telecom_satellite,
      green_tech,
      arable_land_agency,
      clinical_research_center,
      specialized_police_training,
      adv_engineering_corps,
      wars_won,
      wars_lost,
      tax_id,
      alliance_seniority
    }
  }
}
"""

        # 0.1: Call the API.
        async with aiohttp.ClientSession() as sessions:
            async with sessions.post(url=endpoint_url,json={"query":query}) as response:
                data = await response.json()

        # 0.2: Prepare and return the data.
        return data["data"]["nations"]["data"]

    @staticmethod
    async def cata_bot_discord(nation_id):
        """
            Calls discord user information on specific nation from
            Cata Bot api.

            TODO: Add fallback when API returns an error of "nation not in database."
                  Return null, or something.
        """
        # 0: Variables.
        endpoint_url = f"https://cotl.pw/api/discord-user/{nation_id}"

        # 1: Call the API
        async with aiohttp.ClientSession() as sessions:
            async with sessions.get(url=endpoint_url) as response:
                data = await response.json()

        # 2: Prepare and return the data.
        return data


class Adapters:
    """
        This is the adapters which combine and make Helpers useful. This is called by
        either the commands or running tasks.

        TODO LEARN: Why does Pylint return a "R0201: Method could be a function"
                    on these functions.
    """
    @staticmethod
    async def pull_api_information(alliance_id):
        """
            Adapter: Initiate the pulling of the information needed from P&W GraphQl API.
            This adapter is frequently called as the latest information is needed.
        """
        # 0.1: Variables
        default_database = 'main-database'

        # 0.2: Authenticate with the database. (MongoDB)
        db_login_user = f'{os.getenv("DEF_MONGO_USERNAME")}:{os.getenv("DEF_MONGO_PASSWORD")}'
        db_address = f'{os.getenv("DEF_MONGO_URI")}/{default_database}'
        db_login_string = f'mongodb+srv://{db_login_user}@{db_address}?retryWrites=true&w=majority'
        client = motor.motor_asyncio.AsyncIOMotorClient(db_login_string)

        # 1.0: Get Nation Information.
        nation_information = await Helpers.stnd_nation_information(alliance_id)
        # 1.1: Store Nation Information to database.
        db_conn = client['mastersheet-engine'][f'{alliance_id}-nations-information']
        for entry in nation_information:
            await db_conn.find_one_and_update(
                {'nation_id': entry['nation_id']},
                {'$set': entry},
                upsert=True
            )

    @staticmethod
    async def pull_cata_bot_discord(alliance_id):
        """
            Adapter: Responsible for pulling discord user information from Cata Bot API.
            This is called once a day or on demand.
        """
        # 0.0: Variables.
        default_database = 'main-database'
        # 0.1: Authenticate with the database. (MongoDB)
        db_login_user = f'{os.getenv("DEF_MONGO_USERNAME")}:{os.getenv("DEF_MONGO_PASSWORD")}'
        db_address = f'{os.getenv("DEF_MONGO_URI")}/{default_database}'
        db_login_string = f'mongodb+srv://{db_login_user}@{db_address}?retryWrites=true&w=majority'
        client = motor.motor_asyncio.AsyncIOMotorClient(db_login_string)

        # 1.0: Get Nation Information.
        db_conn = client['mastersheet-engine'][f'{alliance_id}-nations-information']
        alliance_nations = await db_conn.find(projection={'nation_id':True,}).to_list(length=None)

        # 2.0: Iterate thourgh all alliance nations and call API.
        for nation in alliance_nations:
            response = await Helpers.cata_bot_discord(nation['nation_id'])
            # check if response has key "error", return value if true.
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
                {'nation_id': nation['nation_id']},
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

            TODO: Breakdown function into sub-functions for easier modifications, etc.
        """
        # 0: Variables
        bot_latency = round(self.bot.latency * 1000)

        await Adapters.pull_api_information(alliance_id=alliance_id)
        await Adapters.pull_cata_bot_discord(alliance_id=alliance_id)
        await ctx.send(f'Mastersheet Engine has been called for {alliance_id}. | {bot_latency}')



def setup(bot):
    """
        Function that is called when the cog is loaded.
    """
    bot.add_cog(MastersheetEngine(bot))
