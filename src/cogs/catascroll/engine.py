import discord
from discord.ext import commands

class Engine(commands.Cog, name="CataScroll: Engine"):
    """
        CataScroll: Engine is responsible for pulling the required information
        from the Politics and War API and storing it in the database.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="csengine")
    async def cs_engine(self, ctx, action:str="status"):
        """
            Used for interacting with the CataScroll Engine.

            @param action: The action to be performed.
              - status (default): Returns the status of the engine,
              - start: if not running, starts the engine,
              - stop: if running, stops the engine,
              - restart: if running, stops the engine and starts it again.
        """
        if action == "status":
            await ctx.send("Status: Under development.")
        elif action == "start":
            await ctx.send("Starting the engine...")
        elif action == "stop":
            await ctx.send("Stopping the engine...")
        elif action == "restart":
            await ctx.send("Restarting the engine...")
        else:
            await ctx.send("Invalid action.")


    @tasks.loop(minutes=10)
    async def engine_runner(self):
        """
            CataScroll Engine Runner is responsible for controlling Puller and Pusher. 
        """
        
