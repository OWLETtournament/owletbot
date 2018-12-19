# -*- coding: UTF-8 -*-

import discord
from discord.ext import commands

from cogs.utils.enums import TradeEmotes


class TradingSystem:
    """The trading/dropping/picking up system for OWLET."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='diamondgraduate')
    async def diamond_graduate(self, ctx, name):
        servericon = ctx.guild.icon_url
        diamond_em = discord.Embed(colour=discord.Colour.teal(),
                                   description=f"Congrats to {name} on achieving Diamond! <:diamond:474220321562558464>")
        diamond_em.set_author(name="Minors Player Graduate!", icon_url=servericon)
        channel = ctx.guild.get_channel(511076448388251669)
        await channel.send(embed=diamond_em)

    @commands.command(name='mastersgraduate')
    async def masters_graduate(self, ctx, name):
        servericon = ctx.guild.icon_url
        masters_em = discord.Embed(colour=discord.Colour.dark_gold(),
                                   description=f"Congrats to {name} on achieving Masters! <:masters:525060384504414208>")
        masters_em.set_author(name="Majors Player Graduate!", icon_url=servericon)
        channel = ctx.guild.get_channel(511076448388251669)
        await channel.send(embed=masters_em)

    @commands.command(name='release', aliases=['drop'])
    async def release(self, ctx, btag, team):
        """Display that a player is being released by x team.

        :param btag: Battle-tag of the player
        :param team: Team being released from
        """

        rem = discord.Embed(colour=discord.Colour.red())
        rem.description = f"{TradeEmotes.bnet} {btag}\n" \
            f"{TradeEmotes.declined} {team}"
        rem.set_author(name="OWLET Player Drop", icon_url=ctx.guild.icon_url)

        channel = ctx.guild.get_channel(511076448388251669)
        await channel.send(embed=rem)

    @commands.command(name='pickup', aliases=['sign'])
    async def pickup(self, ctx, btag, team):
        """Display that a player is being signed by x team.

        :param btag: Battle-tag of the player
        :param team: Team being signed to
        """

        rem = discord.Embed(colour=discord.Colour.green())
        rem.description = f"{TradeEmotes.bnet} {btag}\n" \
            f"{TradeEmotes.accepted} {team}"
        rem.set_author(name="OWLET Player Pickup", icon_url=ctx.guild.icon_url)

        channel = ctx.guild.get_channel(511076448388251669)
        await channel.send(embed=rem)

    @commands.command(name='trade', aliases=['transfer'])
    async def trade(self, ctx, btag, origin, destination):
        """Display that a player is being traded by x team to y team.

        :param btag: Battle-tag of the player
        :param origin: Team being released from
        :param destination: Team being traded to
        """

        rem = discord.Embed(colour=discord.Colour.gold())
        rem.description = f"{TradeEmotes.bnet} {btag}\n" \
            f"{TradeEmotes.declined} {origin}\n" \
            f"{TradeEmotes.accepted} {destination}"
        rem.set_author(name="OWLET Player Transfer", icon_url=ctx.guild.icon_url)

        channel = ctx.guild.get_channel(511076448388251669)
        await channel.send(embed=rem)


def setup(bot):
    bot.add_cog(TradingSystem(bot))

