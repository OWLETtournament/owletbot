import discord
from discord.ext import commands
import json
from cogs.utils import timeconv
from datetime import datetime, timedelta
import asyncio


class Reminders:
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.__remind_checker)

    @commands.command()
    async def remindme(self, ctx, time: timeconv.ConvertStrToTime=None, *, reminder=None):
        """Reminds you after x time

        member - A member of the discord
        time - Time to mute for (almost any imaginable format!)
        reminder - dafuq did you want it for?"""

        if not time:
            return await ctx.send(f'{ctx.author.mention}, you are missing the time!')
        if not reminder:
            return await ctx.send(f'{ctx.author.mention}, you are missing the reminder message!')

        remind_time = timedelta(seconds=time)
        dt = datetime.utcnow() + remind_time
        ft = {
            "year": dt.year,
            "month": dt.month,
            "day": dt.day,
            "hour": dt.hour,
            "minute": dt.minute,
            "second": dt.second,
            "microsecond": dt.microsecond
            }
        try:
            with open('data/reminders.json', "w+") as f:
                data = json.load(f)
                if not ctx.author.id not in data.keys():
                     data[str(ctx.author.id)] = []
                data[str(ctx.author.id)].append({
                    "reminder": reminder,
                    "time": ft
                })
                json.dump(data, f)
        except Exception as e:
            with open('data/reminders.json', 'w+') as f:
                f.write("{}")
            print(e)

        await ctx.author.send(f"A reminder for {datetime(**ft).strftime('%b-%d-%Y %H:%M')} UTC has been set.")

    async def __remind_checker(self):
        await self.bot.wait_until_ready()
        gld = self.bot.get_guild(443126056766013442)

        while not self.bot.is_closed():
            with open('data/reminders.json', "r") as f:
                data = json.load(f)
                for key, value in data:
                    for pos, info in enumerate(value):
                        if (datetime(**info['time']) - datetime.utcnow()).seconds < 0:
                            mb = gld.get_member(key)
                            await mb.send(embed=f"Hi, you wanted me to remind you about: ```{info['reminder']}```")
                            value.pop(pos)
            await asyncio.sleep(15)


def setup(bot):
    bot.add_cog(Reminders(bot))
