import asyncio
import json
from datetime import datetime, timedelta

import discord


class ModmailChecker:
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.__remind_checker())

    async def on_message(self, message):
        if message.channel.category.name.lower() != "mod mail":
            return
        if not message.content.lower().startswith("?reply"):
            with open('data/modmails.json', "r") as f:
                data = json.load(f)
            if str(message.channel.id) not in data:
                return
            data.pop(str(message.channel.id))
            with open('data/modmails.json', 'w') as f:
                json.dump(data, f)

    async def __remind_checker(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(443126056766013442)

        while not self.bot.is_closed():
            with open('data/modmails.json', "r") as f:
                data = json.load(f)
                for channel_id, time in data.items():
                    if ((datetime(**time)) - datetime.utcnow()).total_seconds() < 0:
                        channel = guild.get_channel(channel_id)
                        await channel.send(f"Hi. Make sure to respond to this thread!")
                        data.pop(channel_id)
            with open("data/reminders.json", "w") as f:
                json.dump(data, f, indent=2)

            await asyncio.sleep(15)

    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        if not channel.category.name.lower() == "mod mail" and not isinstance(channel, discord.TextChannel):
            return
        remind_time = timedelta(minutes=2)
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
        with open('data/modmails.json', "r") as f:
            data = json.load(f)
        if channel.id not in data.keys():
            data[str(channel.id)] = ft
        with open('data/modmails.json', 'w') as f:
            json.dump(data, f, indent=2)


def setup(bot):
    bot.add_cog(ModmailChecker(bot))
