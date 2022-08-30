import discord
from datetime import datetime

class SpecificError():
    """
        Called by the on_command_error function in main.py.
        Sends a specific error message to the user.
    """

    async def command_cooldown(self, ctx, error):
        """
            Called when user tries to execute a command in cooldown.
        """
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24

        embed = discord.Embed(
            title="🛑 On Cooldown",
            description=(
                "The command you are trying to execute is on cooldown.\n"
                "Try executing it again later."
            ),
            color=0xfde047, # Tailwind CSS Yellow-300
        )
        embed.add_field(
            name="Time Left",
            value=f"{hours}h, {minutes}m, {seconds}s",
            inline=False,
        )
        embed.add_field(
            name="✉ Contact",
            value="If you think this is an error, contact `@chof64#4021`.",
            inline=False,
        )

    async def no_permissions(bot, ctx, error):
        """
            Called when user tries to execute a command without the required
            permissions.
        """
        embed=discord.Embed(
            title="❌Access Denied",
            description=(
                "You don't have enough permissions to execute this command.\n\n"
                "This action has been logged."
            ),
            color=0xef4444, # Tailwind CSS Red 500
        )
        embed.add_field(
            name="Error Message",
            value=f"```{str(error)}```",
            inline=False,
        )
        embed.add_field(
            name="✉ Contact",
            value="If you think this is an error, contact `@chof64#4021`.",
            inline=False,
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        command=ctx.command.qualified_name
        latency=round(bot.latency * 1000)
        embed.set_footer(text=f"{command} | {latency}")
        embed.timestamp=datetime.utcnow()
        await ctx.send(embed=embed)