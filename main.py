"""
./main.py

Main entrypoint for the application.
"""

import asyncio
import os
import platform

import discord
from discord.ext import commands
from dotenv import load_dotenv

from core.error import ErrorHandler

load_dotenv()

DESCRIPTION = "Hecate is a Discord bot that interacts with Politics and War API to get information."
intents = discord.Intents.default()
intents.message_content = True  # pylint: disable=assigning-non-slot

bot = commands.Bot(
    command_prefix=os.getenv("BOT_PREFIX"), intents=intents, description=DESCRIPTION
)


@bot.event
async def on_ready():
    """
    Executed when the bot is ready.
    """
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

    await bot.tree.sync()
    await bot.change_presence(
        status=discord.Status.dnd, activity=discord.Game(name="with the API")
    )


@bot.event
async def on_message(message):
    """
    Executed everytime a message is sent in a channel.
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_completion(ctx):
    """
    Executed everytime a command is completed.

    TODO: Add logging to `commands-monitor` channel.
    """
    await ctx.message.add_reaction("\U0001F44D")


@bot.event
async def on_command_error(ctx, error):
    """
    Executed everytime a command has an error.

    TODO: Add logging to their respective channels based on error type.
    """
    await ErrorHandler(bot).handle(ctx, error)


async def load_cogs():
    """
    Load all cogs.

    # TODO: Monitor if there are any other uncaught errors.
    """
    for filename in os.listdir("./core/cogs"):
        # ignore if filename is __init__.py
        if filename.endswith(".py") and filename != "__init__.py":
            extension = filename[:-3]
            try:
                await bot.load_extension(f"core.cogs.{extension}")
                print(f"🟢 Loaded core.cogs.{extension}")
            except commands.ExtensionFailed as error:
                print(f"🔴 Failed to load core.cogs.{extension} \n==> {error}")
            except commands.NoEntryPointError as error:
                print(f"🟠 core.cogs.{extension}: No Entry Point \n==> {error}")
            except commands.ExtensionAlreadyLoaded as error:
                print(f"🔵 core.cogs.{extension} is already loaded. \n==> {error}")

    #! TEMP: Load non-core cogs.
    directories = ["catascroll"]
    for directory in directories:
        for filename in os.listdir(f"./cogs/{directory}"):
            if filename.endswith(".py") and filename != "__init__.py":
                extension = filename[:-3]
                try:
                    await bot.load_extension(f"cogs.{directory}.{extension}")
                    print(f"🟢 Loaded {directory}.{extension}")
                except commands.ExtensionFailed as error:
                    print(f"🔴 Failed to load {directory}.{extension} \n==> {error}")
                except commands.NoEntryPointError as error:
                    print(f"🟠 {directory}.{extension}: No Entry Point \n==> {error}")
                except commands.ExtensionAlreadyLoaded as error:
                    print(f"🔵 {directory}.{extension} is already loaded. \n==> {error}")


asyncio.run(load_cogs())
bot.run(os.getenv("BOT_TOKEN"))
