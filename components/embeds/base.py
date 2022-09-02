"""
.
"""
from datetime import datetime

import discord


class GlobalEmbed:  # pylint: disable=too-few-public-methods
    """
    This is used by almost all embed creation.
    This contains the base template for all embeds.
    """

    def __init__(self, bot):
        self.bot = bot

    async def base_global(self, ctx, *, title, description, color):
        """
        The base template for embeds.
        Sets author, footer, and timestamp.
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
        )
        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar.url,
        )
        embed.set_footer(
            text=f"{ctx.command.qualified_name} | {round(self.bot.latency * 1000)}ms"
        )
        embed.timestamp = datetime.utcnow()
        return embed
