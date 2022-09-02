"""
Called by the `core/error/handler` when an uncaught error is encountered.
"""

import os

from dotenv import load_dotenv
from components.embeds import GlobalEmbed

load_dotenv()


class UncaughtLogger:  # pylint: disable=too-few-public-methods
    """
    If app raises an error, but don't have any specific logger,
    it will be sent to this logger instead.
    """

    def __init__(self, bot):
        self.bot = bot

    async def uncaught(self, ctx, error):
        """
        Informs the user about the uncaught error, as well as logs it
        in the backend.
        """
        # BASE
        embed = await GlobalEmbed(self.bot).base_global(
            ctx,
            title="🛑An unknown error has occured.",
            description=(
                "An unknown error has occured when trying to execute "
                "the command you entered.\n"
                "Please make sure that you've entered the command correctly.\n"
                "*Note that commands are case-sensitive*."
            ),
            color=0xD946EF,  # Fuchsia 500 (Tailwind CSS)
        )
        embed.add_field(
            name="💬Error Message",
            value=f"```{error}```",
            inline=False,
        )
        # CLIENT
        client_embed = embed
        await ctx.send(embed=client_embed)
        # BACKEND
        backend_embed = embed
        backend_embed.add_field(
            name="🔹Debug: Command",
            value=(
                "**Command: Raw Message**"
                f"```{ctx.message.content}```"
                "**Command: Cog Name**"
                f"```{ctx.command.cog_name}```"
                "**Command: Qualified Name**"
                f"```{ctx.command.qualified_name}```"
            ),
            inline=False,
        )
        backend_embed.add_field(
            name="🔹Debug: Author",
            value=(
                "**Author: Name**"
                f"```{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.display_name})```"
                "**Author: ID**\n"
                f"```{ctx.author.id}```"
                "**Server: Name**"
                f"```{ctx.message.guild.name}```"
                "**Server: ID**\n"
                f"```{ctx.message.guild.id}```"
                "**Channel: Name**\n"
                f"```{ctx.message.channel.name}```"
                "**Channel: ID**\n"
                f"```{ctx.message.channel.id}```"
            ),
            inline=False,
        )
        await self.bot.get_channel(int(os.getenv("LOGS_GENERAL_ERRORS"))).send(
            embed=backend_embed
        )
