
from datetime import datetime
from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()


class coreOwner(commands.Cog, name="coreowner"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='ping', hidden=True)
    # @commands.is_owner()
    @commands.has_any_role(">> L10 <<",">> SUDO <<")
    async def botPing(self, ctx):
        embed = discord.Embed(
            title="Hecate is online!", 
            description="Hecate is up and always watching.", 
            color=0xFBFBFF
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        # set thumbnail to bot avatar
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f'{ctx.command.qualified_name}  |  {self.bot.latency * 1000:.0f}')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(coreOwner(bot))
    