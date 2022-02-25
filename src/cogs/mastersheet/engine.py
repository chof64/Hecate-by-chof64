
"""
    ./src/cogs/mastersheet/engine.py

    Engine for the mastersheet. Will be used as the
    backend for the Cataclysm Intelligence Division (CID) Mastersheet.
"""

import os
from datetime import datetime

import aiohttp
import discord
import motor.motor_asyncio
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()


class Helpers():
    """
        Functions that do the heavy lifting, and is managed by Adapters.
        These are called by Adapters to get the data needed.

        - stnd_nation_information
        - cata_bot_discord
    """
    # 0: Standard Nation Information (P&W GraphQL).
    async def stnd_nation_information(self, alliance_id):
        """
            Standard Nation Information (P&W GraphQL)

            INFORMATION SCOPE:
            - Expanded Nation Information
            - Expanded Cities Information
            - Minimum Wars Information (Link to War Information)

            TODO: Test this function to see if it works.
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
        data = data["data"]["nations"]["data"]
        return data


    async def cata_bot_discord(self, nation_id):
        """
            Calls discord user information on specific nation from
            Cata Bot api.
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
        Adapters

        TABLE OF CONTENTS:
        - pull_api_information
    """
    async def pull_api_information(self, alliance_id):
        """
            Pulls the API information for the mastersheet.
        """
        # 0.1: Variables
        default_database = 'mastersheet-engine'

        # 0.2: Initialize and authenticate with the database. (MongoDB)
        db_login_user = f'{os.getenv("DEF_MONGO_USERNAME")}:{os.getenv("DEF_MONGO_PASSWORD")}'
        db_address = f'{os.getenv("DEF_MONGO_URI")}/{default_database}'
        db_login_string = f'mongodb+srv://{db_login_user}@{db_address}?retryWrites=true&w=majority'

        client = motor.motor_asyncio.AsyncIOMotorClient(db_login_string)

        # 1.0: Get Nation Information.
        nation_information = await Helpers.stnd_nation_information(self, alliance_id)
        # 1.1: Store Nation Information to database.
        db_conn = client['mastersheet-engine'][f'{alliance_id}-nations-information']

        for entry in nation_information:
            await db_conn.find_one_and_update(
                {'nation_id': entry['nation_id']},
                {'$set': entry},
                upsert=True
            )

    async def pull_cata_bot_discord(self):
        pass


class MastersheetEngine(commands.Cog, name="coreowner"):
    """
        Main class for all command functions. This is where the bot
        interacts when a user initiates a command found in this cog.
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
        await Adapters.pull_api_information(self, alliance_id=alliance_id)


def setup(bot):
    """
        Function that is called when the cog is loaded.
    """
    bot.add_cog(MastersheetEngine(bot))
