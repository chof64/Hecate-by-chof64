"""
WIP
"""
from discord.ext import commands


class Engine(commands.Cog, name="CataScroll: Engine"):
    """
    CataScroll: Engine

    The backend for CataScroll: Mastersheet. Handles all
    CRUD operations from PnW API to Hecate Database.
    """

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    """
    Cog setup function.
    """
    await bot.add_cog(Engine(bot))
