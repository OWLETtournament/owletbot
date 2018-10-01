import discord
from discord.ext import commands
import sys
import traceback
from data import config


def get_prefix(bot, message):
    """Callable Prefix"""

    prefixes = config.prefix

    return commands.when_mentioned_or(*prefixes)(bot, message)


cogs = config.cogs

bot = commands.Bot(command_prefix=get_prefix, description=cogs.description,
                   case_insensitive=True, pm_help=True)

if __name__ == '__main__':
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load cog {cog}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    """When bot started up"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    game = discord.Game(name='OWLET games on Sun, Mon and Tues', type=1,
                                                url='https://twitch.tv/OwletTournament')

    await bot.change_presence(activity=game)
    print(f'Successfully logged in and booted...!')


bot.run(config.token, bot=True, reconnect=True)
