
"""
    ./src/main.py

    The main file for the bot. This is the file that is called to start
    the bot.
"""

from datetime import datetime
import os
import platform
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from dotenv import load_dotenv
import discord


load_dotenv()


intents = discord.Intents.default()
bot = Bot(command_prefix=os.getenv("BOT_PREFIX"), intents=intents)


@bot.event
async def on_ready():
    """
        Function that is called when the bot is ready.

        TODO: Send startup messsage to specified channel.
    """
    # Startup message and information to console.
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

    # Tasks to be initialized on startup.
    bot_presence.start()


@tasks.loop(hours=24)
async def bot_presence():
    """
        Tasked function that control the bot's presence, and activity message.

        TODO: [FIX] CustomActivity message not working.
        TODO: CustomActivity showing environment resources (CPU, RAM, etc.)
    """
    activity_output = "This is a test. discord.CustomActivity"
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.CustomActivity(name=activity_output)
    )


if __name__ == "__main__":

    cogWhitelist = ["core"]

    # Load bot cog files, if white-listed.
    for ent in cogWhitelist:
        for file in os.listdir(f"./src/cogs/{ent}"):
            if file.endswith(".py"):
                ext = file[:-3]
                try:
                    bot.load_extension(f"cogs.{ent}.{ext}")
                    print(f"Loaded extension '{ent}.{ext}'")
                except Exception as e:
                    excptn = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {ent}.{ext}\n{excptn}")


@bot.event
async def on_message(message):
    """
        Function that is called when a message is sent to a channel that the bot has permissions on.
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_completion(ctx):
    """
        Function that is called when a command was successfully ran.

        TODO: Add file logging feature, to log all commands successfully ran by users in a file,
              for long term storage. For audit purposes.
    """
    executed_command = ctx.command.qualified_name
    print(f"""{datetime.utcnow()}:
                Executed {executed_command}
                command in {ctx.guild.name} (ID: {ctx.message.guild.id})
                by {ctx.message.author} (ID: {ctx.message.author.id})""")


@bot.event
async def on_command_error(ctx, error):
    """
        Function that is called when a command is ran, but encounters an error.

        TODO: Work to sort out this code and make it more readable.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"""You can use this command again in
            {f'{round(hours)} hours' if round(hours) > 0 else ''}
            {f'{round(minutes)} minutes' if round(minutes) > 0 else ''}
            {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.""",
            color=0xD17B0F
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        command_path = ctx.command.qualified_name
        bot_latency = bot.latency * 1000
        embed.set_footer(text=f'{command_path}  |  {bot_latency}')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=0xD17B0F
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        command_path = ctx.command.qualified_name
        bot_latency = bot.latency * 1000
        embed.set_footer(text=f'{command_path}  |  {bot_latency}')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xD17B0F
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        command_path = ctx.command.qualified_name
        bot_latency = bot.latency * 1000
        embed.set_footer(text=f'{command_path}  |  {bot_latency}')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Uncaught Error",
            description=f'```{error}```',
            color=0xBC2C1A
            )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        command_path = ctx.command.qualified_name
        bot_latency = bot.latency * 1000
        embed.set_footer(text=f'{command_path}  |  {bot_latency}')
        embed.timestamp = datetime.utcnow()
        channel_id = os.getenv('BOT_ERROR_CHANNEL')
        await bot.get_channel(int(channel_id)).send(embed=embed)
        raise error


bot.run(os.getenv('BOT_TOKEN'))
