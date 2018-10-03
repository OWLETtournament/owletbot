from discord.ext import commands
import discord


class TradingSystem:
    """The trading/dropping/picking up system for OWLET."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='diamondGraduate')
    async def diamond_graduate(self, ctx, name: str):
        servericon = ctx.message.server.icon_url
        diamond_em = discord.Embed(colour=0x8ce9ff, description="Congrats to " + discordTag.content +
                                                                " on achieving Diamond! <:diamond:474220321562558464> ")
        diamond_em.set_author(name="OWLET Player Graduate!", icon_url=servericon)
        channel = ctx.guild.get_channel(472450201009782787)
        await channel.send(embed=diamond_em)


def setup(bot):
    bot.add_cog(TradingSystem(bot))

