import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from collections import defaultdict
import datetime
import os


class Report:
    """Commands for the OWLET report system"""

    default = {}

    def __init__(self, bot):
        db = dataIO.load_json("data/reports/users.json")
        self.bot = bot
        default = {}
        self.db = defaultdict(lambda: default.copy(), db)

    async def _get_warnings(self, ctx, user):
        if user.id not in self.db:
            await self.bot.send_message(ctx.message.channel, f"{user} does not have any reports on file.")
            return None
        else:
            y = []
            for x in self.db[user.id]["warn-reasons"]:
                y.append(x)
            return y

    async def _append_warnings(self, ctx, user, reason):
        if user.id not in self.db:
            self.db[user.id] = {}
            self.db[user.id]["warnings"] = '1'
            self.db[user.id]["warn-reasons"] = {}
            self.db[user.id]["warn-reasons"][reason] = {}
            self.db[user.id]["warn-reasons"][reason] = ctx.author.id  # Silent logger

        else:
            self.db[user.id]["warnings"] = str(int(self.db[user.id]["warnings"]) + 1)
            self.db[user.id]["warn-reasons"][reason] = ctx.author.id

        self.save()

    @commands.command(name='userInfo')
    @commands.has_any_role('Tournament Support', 'Admin', 'Moderator', 'Director')
    async def user_info(self, ctx, *, user: discord.Member):
        warnings = await self._get_warnings(ctx, user)

        if warnings is None:
            return

        e = discord.Embed(colour=0xF7DC6F, timestamp=datetime.datetime.utcnow())
        e.set_author(name=str(user), icon_url=user.avatar_url)
        e.set_footer(text=f'Requested by {ctx.message.author.name} at')

        x = 1
        for i in warnings:
            e.add_field(name=f'Warning {x}', value=i, inline=True)
            x += 1

        await ctx.send(embed=e)

    @commands.command(name='warnUser')
    @commands.has_any_role('Tournament Support', 'Admin', 'Moderator', 'Director')
    async def warn_user(self, ctx, user: discord.Member, *, reason):
        await self._append_warnings(ctx, user, reason)
        await ctx.send(f'Added warning to user {user}')

    @commands.command(name='getRawWarns')
    @commands.has_any_role('Tournament Support', 'Admin', 'Moderator', 'Director')
    async def get_raw_warns(self, ctx):
        with open('data/reports/users.json') as f:
            json_f = discord.File('data/reports/users.json', filename='report_db.json')
            await ctx.send(f'```json\n{f.read()}\n```', file=json_f)

    @commands.command(name='getModModmail')
    @commands.has_any_role('Tournament Support', 'Admin', 'Moderator', 'Director')
    async def get_mod_mail(self, ctx, user: discord.User):
        try:
            with open(f"logs/{user.id}", 'r') as f:
                await ctx.send(f"{f.read()}", file=discord.File(f"logs/{user.id}"))
        except FileNotFoundError:
            await ctx.send('The user has no logs on file.')

    def save(self):
        dataIO.save_json("data/reports/users.json", self.db)


def check_folders():
    if not os.path.exists("data/reports"):
        print("Creating data/reports folder...")
        os.makedirs("data/reports")


def check_files():
    if not dataIO.is_valid_json("data/reports/users.json"):
        print("Creating empty data/reports/users.json")
        dataIO.save_json("data/reports/users.json", {})


def setup(bot):
    bot.add_cog(Report(bot))
