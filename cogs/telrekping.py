import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import box, pagify
from copy import deepcopy
from collections import defaultdict
import asyncio
import logging
import logging.handlers
import random
import os
import datetime
import re
from datetime import datetime

class TelrekPinger:
    """Self ToS Role assignment system. ~Danners"""

    default = {}

    def __init__(self, bot):
        self.bot = bot

    async def spamTelrek(self, message):
        if message.author.id == '295001068407095296':
            await self.bot.send_message(message, f'{message.author.mention} dont ping me again')

def setup(bot):
    n = TelrekPinger(bot)
    bot.add_cog(n)
    bot.add_listener(n.spamTelrek, "on_message")
