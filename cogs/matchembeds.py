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
from oauth2client.service_account import ServiceAccountCredentials
import gspread

class MatchEmbeds:
    """OWLETBot Match Embed Poster"""

    default = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_any_role("Tournament Support", "Admin")
    async def matchEmbeds(self, ctx):

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('data/gsheets/client-secret.json', scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_key("1RLYzd6-IaAz1etT-7DlHd8E8yy-sL2nUcsq6Yf5kyIs").worksheet("Bot Code")

        listOfHashes = sheet.get_all_values()

        await self.bot.say("What day is it?\n```1 - Wk 1 Day 1\n2 - Wk 1 Day 2\n3 - Wk 2 Day 1\n4 - Wk 2 Day 2\n"
                           "5 - Wk 3 Day 1\n6 - Wk 4 Day 2```")

        global game
        game = 1

        dayCode = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)
        if not dayCode:
            await self.bot.say("Timed out.")
            return
        if str(dayCode.content) not in ['1', '2', '3', '4', '5', '6']:
            await self.bot.say("Please enter a number 1-6 next time. Command cancelling.")
            return
        else:
            for i in range(1, 50):

                values = listOfHashes[i]

                global dayValue
                dayValue = values[19]

                if dayValue is not None:
                    print(f"Row # {str(game)} - {dayValue}")
                    if values[3] == dayCode.content:

                        matchInfo = discord.Embed(colour=0xA2D9CE)

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
                        matchMessage = await self.bot.send_message(self.bot.get_channel('476764717369655303'), embed=matchInfo)
                        sheet.update_cell(game, 20, matchMessage.id)
                        print(f'Match {matchMessage.id} successfully sent.')
                        await asyncio.sleep(1)
                        pass
                game = game + 1
            return




def setup(bot):
    n = MatchEmbeds(bot)
    bot.add_cog(n)