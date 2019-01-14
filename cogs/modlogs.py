import os
from random import randint

import asyncpg
import discord
from discord.ext import commands

# For IDE support
from bot import Bot


class ModLogs:

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("Director", "Admin", "Tournament Support")
    async def userid(self, ctx, user: discord.Member):
        """Get the user ID."""
        pool = self.bot.connections['owlet']
        ids = []
        async with pool.acquire() as con:
            async with con.transaction():
                async for log in con.cursor(f'SELECT * FROM modmail_log WHERE id = {user.id}'):
                    ids.append(log['id'])

        warn = False
        if user.id not in ids:
            warn = True

        await ctx.send(f"That user's ID is `{user.id}`. {'*They do not have a modmail on file.*' if warn else ''}")

    @commands.command()
    @commands.has_any_role("Director", "Admin", "Tournament Support")
    async def modmails(self, ctx: commands.Context, *, user: discord.Member):
        """Get the modmails of a user.

         user: Any user in this Discord."""

        pool = self.bot.connections['owlet']
        logs = []
        try:
            async with pool.acquire() as con:
                async with con.transaction():
                    async for log in con.cursor(f'SELECT * FROM modmail_log WHERE id = {user.id}'):
                        logs.append(log['log'])
        except asyncpg.exceptions.InterfaceError:
            self.bot.connections = await self.bot.setup_db(['owlet'])
            return await ctx.invoke(self.bot.get_command('modmails'), user=user)

        # Format log + write to temp file
        logs = '\n'.join(logs)
        rand = randint(1000, 9999)
        fp = f'temp-{rand}.txt'
        with open(fp, 'w') as f:
            f.write(logs)

        await ctx.send(file=discord.File(fp, filename=f'{user.id}-modmail.txt'))

        os.remove(fp)

    @commands.command(name='dice')
    async def dice(self, ctx, sides=None):
        """Rolls a virtual dice.

        Formatted in ?dice {d[sides] | [sides]} format."""

        import random

        if sides is None:
            sides = 6
        else:
            sides = sides.split("d")
            sides = sides[-1]
        num = random.randint(1, int(sides))

        await ctx.send(embed=discord.Embed(colour=0x36393E, description='\U0001f3b2 || The dice lands on: **'
        f'{num}**'))


def setup(bot):
    bot.add_cog(ModLogs(bot))
