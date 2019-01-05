import discord
import os
from discord.ext import commands
from random import randint

# For IDE support
from bot import Bot


class ModLogs:

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("Director", "Admin", "Tournament Support")
    async def modmails(self, ctx: commands.Context, *, user: discord.Member):
        """Get the modmails of a user.

         user: Any user in this Discord."""

        con = self.bot.connections['owlet']
        logs = []
        async with con.transaction():
            async for log in con.cursor(f'SELECT * FROM modmail_log WHERE id = {user.id}'):
                logs.append(log['log'])

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
