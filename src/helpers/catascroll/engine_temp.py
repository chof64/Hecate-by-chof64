
"""
    These contains functions and classes that makes the catascroll.engine_temp
    commands work.

    Main purpose of these functions is to make the main file cleaner and
    easier to read, and have a centralized location for all the functions
    related to this category.

    Functions here are, but not limited to, the main engine function
    wrapped in discord tasks, and the sub-functions that are responsible
    for calling the API and connecting to the database.
"""

from discord.ext import tasks, commands

class EngineMain:
    """
        This is the main entrypoint for the CataScroll: Mastersheet Engine.
        This is called by the cogs to start, stop, or get information about
        its status.
    """

    async def engine_primary():

@tasks.loop(minutes=5)
async def nations_information():
    

