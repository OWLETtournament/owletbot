# -*- coding: UTF-8 -*-

import discord
from discord.ext import commands
import asyncpg
import sys
import traceback
from data import config


def get_prefix(bot, message):
    """Callable Prefix"""

    prefixes = config.prefix

    return commands.when_mentioned_or(*prefixes)(bot, message)


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = {}

    def load_extensions(self, cogs):
        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception:
                print(f'Failed to load cog {cog}.', file=sys.stderr)
                traceback.print_exc()

        self.remove_command('help')
        self.load_extension("jishaku")

    async def on_connect(self):
        game = discord.Game(name='Starting up', type=discord.activity.Streaming,
                            url='https://twitch.tv/OwletTournament')
        await self.change_presence(activity=game, status=discord.Status.idle)

    async def on_ready(self):
        """When bot started up"""

        print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
        game = discord.Game(name='OWLET games on Sat, Sun, Mon and Tues', type=discord.activity.Streaming,
                            url='https://twitch.tv/OwletTournament')
        await self.change_presence(activity=game, status=discord.Status.online)
        print(f'Successfully logged in and booted...!')

        self.connections = await self.setup_db(config.dbs)

    @staticmethod
    async def setup_db(dbs):
        creds = {
            "user": "owlet",
            "password": config.db.pw,
            "host": config.db.host
        }

        return_value = {}

        for db in dbs:
            return_value[db] = await asyncpg.connect(**creds, database=db)

        return return_value


bot = Bot(description=config.description, command_prefix=config.prefix,
          case_insensitive=True, pm_help=True)

bot.load_extensions(config.cogs)

try:
    bot.run(config.token)

except (KeyboardInterrupt, SystemError, SystemExit):
    bot.loop.create_task(bot.logout())
    for conn in bot.connections:
        bot.loop.create_task(conn.close())

finally:
    bot.loop.close()
