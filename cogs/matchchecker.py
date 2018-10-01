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
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
import gspread

class MatchChecker:
    """OWLETBot Match Embed Checker"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("Tournament Support", "Admin", "test")
    async def startChecker(self):
        await self.bot.say("started.")
        while (1):
            for i in range(1, 50):

                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                creds = ServiceAccountCredentials.from_json_keyfile_name('data/gsheets/client-secret-read.json',
                                                                         scope)
                client = gspread.authorize(creds)

                sheet = client.open_by_key("1RLYzd6-IaAz1etT-7DlHd8E8yy-sL2nUcsq6Yf5kyIs").worksheet("Bot Code")

                listOfHashes = sheet.get_all_values()
                values = listOfHashes[i]

                global dayValue
                dayValue = values[19]

                try:
                    print(str(i))

                    dayColour = 0x7FB3D5

                    if dayValue == '1':
                        dayColour = 0xAED6F1
                    elif dayValue == '2':
                        dayColour = 0x7FB3D5
                    elif dayValue == '3':
                        dayColour = 0xF5B7B1
                    elif dayValue == '4':
                        dayColour = 0xD2B4DE
                    elif dayValue == '5':
                        dayColour = 0xA2D9CE
                    elif dayValue == '6':
                        dayColour = 0x85C1E9

                    matchInfo = discord.Embed(colour=dayColour)

                    redTeam = values[0]
                    blueTeam = values[1]
                    matchDate = values[2]
                    matchTime = values[4]
                    matchInfo.set_author(name=f"{matchDate}, {matchTime}")
                    finalScore = f"{redTeam} {values[10]} - {values[16]} {blueTeam}"
                    matchInfo.add_field(name='Series Score', value=finalScore)
                    escortScore = f'<:escort:476213138266783764> {values[5]} - {values[11]}'
                    assaultScore = f'<:2cp:476213138170183704> {values[6]} - {values[12]}'
                    kothScore = f'<:control:476213138161795082> {values[7]} - {values[13]}'
                    hybridScore = f'<:hybrid:476213138203607040> {values[8]} - {values[14]}'
                    tiebreakerScore = f'<:control:476213138161795082> {values[9]} - {values[15]}'
                    combinedScore = f"{escortScore}\n{assaultScore}\n{kothScore}\n{hybridScore}\n{tiebreakerScore}"
                    matchInfo.add_field(name='Map Scores', value=combinedScore, inline=False)
                    oldMessage = values[19]
                    print(oldMessage)
                    storedMessage = await self.bot.get_message(self.bot.get_channel('476764717369655303'),
                                                               oldMessage)
                    await self.bot.edit_message(storedMessage, new_content=None, embed=matchInfo)
                except discord.HTTPException:
                    print('issue')
                    pass


def setup(bot):
    n = MatchChecker(bot)
    bot.add_cog(n)
