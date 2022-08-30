
import discord
from datetime import datetime

class GenericResponse():
    """
        DefaultMessageEmbeds contains default embeds template that
        can be used to send responses.
    """

    async def resp_successful(self, ctx, title:str, description:str):
        """
            Return with custom command response. Successful execution.
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=0x22c55e, # Tailwind CSS Green 500
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.command.qualified_name} | {round(self.bot.latency * 1000)}")
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed=embed)
        # return embed