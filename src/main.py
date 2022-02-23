
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import platform
from datetime import datetime


load_dotenv()


intents = discord.Intents.default()
bot = Bot(command_prefix=os.getenv("BOT_PREFIX"), intents=intents)


@bot.event
async def on_ready():

    # TODO: Startup and login information to be sent on specific channel.
    # NOTE: Output bot information on successful login and startup.
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

    # NOTE: Tasks to be initialized on startup.
    botPresence.start()


@tasks.loop(hours=24)
async def botPresence():

    # TODO: CustomActivity showing environment resources (CPU, RAM, etc.)
    activityOutput = "This is a test. discord.CustomActivity"
    await bot.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name=activityOutput))


if __name__ == "__main__":

    cogWhitelist = ["core"]

    # NOTE: Load bot cog files, if white-listed.
    for entry in cogWhitelist:
        for file in os.listdir(f"./src/cogs/{entry}"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    bot.load_extension(f"cogs.{entry}.{extension}")
                    print(f"Loaded extension '{entry}.{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {entry}.{extension}\n{exception}")


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


# TODO: Add file logging feature, to log all commands ran by users in a file.
@bot.event
async def on_command_completion(ctx):
    executedCommand = ctx.command.qualified_name
    print(f"{datetime.utcnow()}: Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


# TODO: More pretty and universal embed design, uniform design scheme for Errors, Warnings, and Info.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xD17B0F
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.command.qualified_name}  |  {bot.latency * 1000:.0f}')
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
        embed.set_footer(text=f'{ctx.command.qualified_name}  |  {bot.latency * 1000:.0f}')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xD17B0F
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.command.qualified_name}  |  {bot.latency * 1000:.0f}')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
    else: 
        embed = discord.Embed(
            title="Uncaught Error",
            description=f'```{error}```',
            color= 0xBC2C1A
            )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.command.qualified_name}  |  {bot.latency * 1000:.0f}')
        embed.timestamp = datetime.utcnow()
        await bot.get_channel(os.getenv("BOT_ERROR_CHANNEL")).send(embed=embed)
        raise error


bot.run(os.getenv('BOT_TOKEN'))

