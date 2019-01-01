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
            async for log in con.cursor(f'SELECT * FROM modmail_logs WHERE id = {user.id}'):
                logs.append(log['log'])

        # Format log + write to temp file
        logs = '\n'.join(logs)
        rand = randint(1000, 9999)
        fp = f'temp/temp-{rand}.log'
        with open(fp, 'w+') as f:
            f.write(logs)

        await ctx.send(file=discord.File(fp, filename=f'{user.id}-modmail.log'))

        os.remove(fp)


def setup(bot: Bot):
    bot.add_cog(ModLogs(bot))
