"""
./core/extensions.py
"""

from discord.ext import commands


class Extensions(commands.Cog, name="Core: Extensions"):
    """
    Core: Extensions

    Responsible for loading, unloading and reloading non-core extensions/cogs.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="extensions")
    async def extensions(self, ctx):
        """
        Responsible for loading, unloading and reloading non-core extensions/cogs.
        """
        # If no subcommand has been invoked, inform the user
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed...")

    @extensions.command(name="load")
    async def extension_load(self, ctx, extension):
        """
        Loads an extension.
        """
        await self.bot.load_extension(extension)
        await ctx.send(f"{extension}: Loaded")

    @extensions.command(name="reload")
    async def extension_reload(self, ctx, extension):
        """
        Reloads an extension.
        """
        await self.bot.reload_extension(extension)
        await ctx.send(f"{extension}: Reloaded")


async def setup(bot):
    """
    Setup function.
    """
    await bot.add_cog(Extensions(bot))
