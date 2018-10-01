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

class SelfToSRoles:
    """Self ToS Role assignment system. ~Danners"""

    global roleEmote
    roleEmote = ""

    default = {}

    def __init__(self, bot):
        db = dataIO.load_json("data/selftosroles/roles.json")
        self.bot = bot
        self.db = defaultdict(lambda: default.copy(), db)

    @commands.group(pass_context=True)
    async def sendemote(self, ctx):
        """send an emote lol"""

        channel = ctx.message.channel
        channelid = str(channel.id)
        authorid = str(ctx.message.author.id)

        if ctx.invoked_subcommand is None:
            await self.bot.say('Current emotes: `partyblobs`')
        else:
            pass

    @sendemote.command()
    async def partyblobs(self):
        """lol what"""

        emoteLib = discord.Server(id='401122122400923648')

        animpartyblob1 = discord.Emoji(name='animpartyblob1', server=emoteLib)
        pbID = str(animpartyblob1.id)

        await self.bot.say("<a:animpartyblob1:401122373236948993> <a:animpartyblob2:401122373367234570> "
                           "<a:animpartyblob3:401122373396463616> <a:animpartyblob4:401122373262376971> "
                           "<a:animpartyblob5:401122373425823744> <a:animpartyblob6:401122373614567434> "
                           "<a:animpartyblob7:401122373698322432> <a:animpartyblob8:401122373270503427> "
                           "<a:animpartyblob9:401122373434343431>")

    @sendemote.command()
    async def ADDblobs(self):
        """lol what"""

        emoteLib = discord.Server(id='401122122400923648')

        animpartyblob1 = discord.Emoji(name='animpartyblob1', server=emoteLib)
        pbID = str(animpartyblob1.id)

        await self.bot.say("<a:animpartyblob1:401122373236948993> <a:animpartyblob1:401122373236948993> "
                           "<a:animpartyblob1:401122373236948993> <a:animpartyblob1:401122373236948993> "
                           "<a:animpartyblob1:401122373236948993> <a:animpartyblob1:401122373236948993> "
                           "<a:animpartyblob1:401122373236948993> <a:animpartyblob1:401122373236948993>")
        await self.bot.say("<@124644921700253696> <@124644921700253696> <@124644921700253696> "
                           "lol bad telrek is right ur wrong :)))))")
        await self.bot.say("<@124644921700253696> <@124644921700253696> <@124644921700253696> "
                           "lol bad telrek is right ur wrong :)))))")

    @sendemote.command()
    async def telrekblob(self):
        """telrek?"""

        emoteLib = discord.Server(id='401122122400923648')

        await self.bot.say("<a:telrekblob:466385475935141889>")

    @sendemote.command()
    async def nekkrachan(self):
        """nekkra-chan?"""

        await self.bot.say("<a:nekkrachan:468578731019993109>")

    @sendemote.command()
    async def dannoCool(self):
        """herro"""

        await self.bot.say("<a:dannoCool:469984853228650496>")

    @sendemote.command()
    async def danno(self):
        """herro normie"""

        await self.bot.say("<a:danno:469984749071499275>")

    @commands.command()
    async def diceroll(self):
        """Rolls a dice."""

        number = random.randint(1, 6)

        await self.bot.say("The die lands on... **" + str(number) + "**.")

    def save(self):
        dataIO.save_json("data/selftosroles/roles.json", self.db)

    @commands.command()
    async def customdiceroll(self, sides : int):
        """Rolls a dice with a custom number of sides."""

        number = random.randint(1, sides)

        await self.bot.say("The weirdly-shaped die lands on... **" + str(number) + "**.")

    @commands.command(pass_context=True)
    async def requestTalk(self, ctx):
        """OWLET Meeting"""

        raisedHand = discord.Role(id="470426997152153610", server="443126056766013442")
        reqSendChannel = self.bot.get_channel('471766673427529734')
        voxChannelMeeting = self.bot.get_channel('464595697442750494')
        voxChannelNest = self.bot.get_channel('443126056766013446')

        await self.bot.send_message(reqSendChannel, "<@" + ctx.message.author.id + "> has requested the microphone.")
        await self.bot.send_message(reqSendChannel, "Please reply with `yes` to give the microphone.")

        await asyncio.sleep(1)

        adminResponse = await self.bot.wait_for_message(timeout=60, channel=reqSendChannel)

        if not adminResponse:
            await self.bot.send_message(reqSendChannel, "Request timed out after 60 seconds.")
            await self.bot.say("<@" + ctx.message.author.id + ">, your request was timed out.")
            return False

        elif adminResponse.clean_content.lower() == 'yes':
            await self.bot.send_message(reqSendChannel, "Microphone has been handed to the requestee.")
            await self.bot.say("<@" + ctx.message.author.id + ">, you may now talk.")
            await self.bot.add_roles(ctx.message.author, raisedHand)

            await self.bot.move_member(ctx.message.author, voxChannelNest)
            await self.bot.move_member(ctx.message.author, voxChannelMeeting)
            return True

        else:
            await self.bot.send_message(reqSendChannel, "Request was denied.")
            await self.bot.say("<#" + ctx.message.author.id + ">, Request was denied.")
            return False

    @commands.command()
    @commands.has_any_role("Admin", "Tournament Support")
    async def revokeTalk(self, user: discord.Member=None):
        """OWLET Meeting"""

        raisedHand = discord.Role(id="470426997152153610", server="443126056766013442")
        voxChannelMeeting = self.bot.get_channel('464595697442750494')
        voxChannelNest = self.bot.get_channel('443126056766013446')

        await self.bot.remove_roles(user, raisedHand)
        await self.bot.move_member(user, voxChannelNest)
        await self.bot.move_member(user, voxChannelMeeting)
        await self.bot.say("Microphone removed.")

    @commands.command(pass_context=True)
    async def givemePUG(self, ctx):

        PUG = discord.Role(id="473929528243388436", server="443126056766013442")
        emote1 = discord.Emoji(id="401122373236948993", server='401122122400923648')
        emote2 = discord.Emoji(id="401122373367234570", server='401122122400923648')
        emote3 = discord.Emoji(id="401122373396463616", server='401122122400923648')
        emote4 = discord.Emoji(id="401122373262376971", server='401122122400923648')
        emote5 = discord.Emoji(id="401122373425823744", server='401122122400923648')
        emote6 = discord.Emoji(id="401122373614567434", server='401122122400923648')
        emote7 = discord.Emoji(id="401122373698322432", server='401122122400923648')
        emote8 = discord.Emoji(id="401122373270503427", server='401122122400923648')
        emote9 = discord.Emoji(id="401122373434343431", server='401122122400923648')

        await self.bot.add_roles(ctx.message.author, PUG)
        await self.bot.add_reaction(ctx.message, emote1)
        await self.bot.add_reaction(ctx.message, emote2)
        await self.bot.add_reaction(ctx.message, emote3)
        await self.bot.add_reaction(ctx.message, emote4)
        await self.bot.add_reaction(ctx.message, emote5)
        await self.bot.add_reaction(ctx.message, emote6)
        await self.bot.add_reaction(ctx.message, emote7)
        await self.bot.add_reaction(ctx.message, emote8)
        await self.bot.add_reaction(ctx.message, emote9)

    @commands.command(pass_context=True)
    async def nomorePUG(self, ctx):

        PUG = discord.Role(id="473929528243388436", server="443126056766013442")
        emote1 = discord.Emoji(id="401122373236948993", server='401122122400923648')
        emote2 = discord.Emoji(id="401122373367234570", server='401122122400923648')
        emote3 = discord.Emoji(id="401122373396463616", server='401122122400923648')
        emote4 = discord.Emoji(id="401122373262376971", server='401122122400923648')
        emote5 = discord.Emoji(id="401122373425823744", server='401122122400923648')
        emote6 = discord.Emoji(id="401122373614567434", server='401122122400923648')
        emote7 = discord.Emoji(id="401122373698322432", server='401122122400923648')
        emote8 = discord.Emoji(id="401122373270503427", server='401122122400923648')
        emote9 = discord.Emoji(id="401122373434343431", server='401122122400923648')

        await self.bot.remove_roles(ctx.message.author, PUG)
        await self.bot.add_reaction(ctx.message, emote1)
        await self.bot.add_reaction(ctx.message, emote2)
        await self.bot.add_reaction(ctx.message, emote3)
        await self.bot.add_reaction(ctx.message, emote4)
        await self.bot.add_reaction(ctx.message, emote5)
        await self.bot.add_reaction(ctx.message, emote6)
        await self.bot.add_reaction(ctx.message, emote7)
        await self.bot.add_reaction(ctx.message, emote8)
        await self.bot.add_reaction(ctx.message, emote9)

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin", "Tournament Support", "Coach", "Team Representative")
    async def playerTrade(self, ctx):
        """Define a player team trade"""

        await self.bot.say("What is the player's battletag?")
        battletag = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not battletag:
            await self.bot.say("Timed out after 60 minutes.")
            return False
        else:
            await self.bot.say("What is the player's discord? (Please @ them such as <@" + ctx.message.author.id + ">)")

        discordtag = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not discordtag:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        else:
            await self.bot.say("What team was the player on **previously**?")

        previousteam = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not previousteam:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        else:
            await self.bot.say("What team is the player being transferred to?")

        newteam = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not newteam:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        else:
            await self.bot.say("What role is the player? (Either `flex`, `dps`, `tank` or `support`)")

        OWrole = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not OWrole:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        elif OWrole.content.lower() not in ['flex', 'dps', 'tank', 'support']:
            await self.bot.say("That is not a valid role. Cancelling.")
            return False
        else:
            await self.bot.say("Please confirm that this is the correct transfer log with `yes`.")

        servericon = ctx.message.server.icon_url



        transferLog = discord.Embed(colour=0xDAA520)
        transferLog.set_author(name="OWLET Player Transfer", icon_url=servericon)

        if OWrole.content.lower() == 'dps':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
<:DPS:474010007537451009>""", inline=True)
        elif OWrole.content.lower() == 'tank':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
<:TANK:474010288371269664>""", inline=True)
        elif OWrole.content.lower() == 'support':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
<:SUPPORT:474010288950083584>""", inline=True)
        elif OWrole.content.lower() == 'flex':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
:recycle:""", inline=True)

        transferLog.add_field(name="Transfer Info", value="<:outtick:472572219734884362> " + previousteam.content + """
<:intick:472572212247920640> """ + newteam.content)

        await self.bot.say(embed=transferLog)

        confirm = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not confirm:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        if confirm.content.lower() != "yes":
            await self.bot.say("Cancelled.")
            return False
        else:
            await self.bot.send_message(self.bot.get_channel('472450201009782787'), embed=transferLog)
            await self.bot.say("Transfer log sent.")

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin", "Tournament Support", "Coach", "Team Representative")
    async def playerDrop(self, ctx):
        """Define a player team trade"""

        await self.bot.say("What is the player's battletag?")
        battletag = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not battletag:
            await self.bot.say("Timed out after 60 minutes.")
            return False
        else:
            await self.bot.say("What is the player's discord? (Please @ them such as <@" + ctx.message.author.id + ">)")

        discordtag = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not discordtag:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        else:
            await self.bot.say("What team was the player on **previously**?")

        previousteam = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not previousteam:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        else:
            await self.bot.say("What role is the player? (Either `flex`, `dps`, `tank` or `support`)")

            OWrole = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

            if not OWrole:
                await self.bot.say("Timed out after 60 seconds.")
                return False
            elif OWrole.content.lower() not in ['flex', 'dps', 'tank', 'support']:
                await self.bot.say("That is not a valid role. Cancelling.")
                return False
            else:
                await self.bot.say("Please confirm that this is the correct transfer log with `yes`.")

        servericon = ctx.message.server.icon_url


        transferLog = discord.Embed(colour=0xDAA520)
        transferLog.set_author(name="OWLET Player Drop", icon_url=servericon)

        if OWrole.content.lower() == 'dps':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
<:DPS:474010007537451009>""", inline=True)
        elif OWrole.content.lower() == 'tank':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
<:TANK:474010288371269664>""", inline=True)
        elif OWrole.content.lower() == 'support':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
<:SUPPORT:474010288950083584>""", inline=True)
        elif OWrole.content.lower() == 'flex':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
:recycle:""", inline=True)

        transferLog.add_field(name="Transfer Info", value="<:outtick:472572219734884362> " + previousteam.content + """
<:intick:472572212247920640> *Free Agent Pool*""")

        await self.bot.say(embed=transferLog)

        confirm = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not confirm:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        if confirm.content.lower() != "yes":
            await self.bot.say("Cancelled.")
            return False
        else:
            await self.bot.send_message(self.bot.get_channel('472450201009782787'), embed=transferLog)
            await self.bot.say("Transfer log sent.")

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin", "Tournament Support", "Coach", "Team Representative")
    async def freeAgentPickup(self, ctx):
        """Define a player team trade"""

        await self.bot.say("What is the player's battletag?")
        battletag = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not battletag:
            await self.bot.say("Timed out after 60 minutes.")
            return False
        else:
            await self.bot.say("What is the player's discord? (Please @ them such as <@" + ctx.message.author.id + ">)")

        discordtag = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not discordtag:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        else:
            await self.bot.say("What team is the player on **now**?")

        previousteam = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not previousteam:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        else:
            await self.bot.say("What role is the player? (Either `flex`, `dps`, `tank` or `support`)")

            OWrole = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

            if not OWrole:
                await self.bot.say("Timed out after 60 seconds.")
                return False
            elif OWrole.content.lower() not in ['flex', 'dps', 'tank', 'support']:
                await self.bot.say("That is not a valid role. Cancelling.")
                return false
            else:
                await self.bot.say("Please confirm that this is the correct transfer log with `yes`.")
        servericon = ctx.message.server.icon_url

        transferLog = discord.Embed(colour=0xDAA520)
        transferLog.set_author(name="OWLET Player Pickup", icon_url=servericon)

        if OWrole.content.lower() == 'dps':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
        <:DPS:474010007537451009>""", inline=True)
        elif OWrole.content.lower() == 'tank':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
<:TANK:474010288371269664>""", inline=True)
        elif OWrole.content.lower() == 'support':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
<:SUPPORT:474010288950083584>""", inline=True)
        elif OWrole.content.lower() == 'flex':
            transferLog.add_field(name="Player Info", value="<:discordlogo:472564767731613697> " + discordtag.content + """ 
<:battlenet:472564730079346699> """ + battletag.content + """
:recycle:""", inline=True)

        transferLog.add_field(name="Transfer Info", value="""<:outtick:472572219734884362> *Free Agent Pool*
<:intick:472572212247920640> """ + previousteam.content)

        await self.bot.say(embed=transferLog)

        confirm = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)

        if not confirm:
            await self.bot.say("Timed out after 60 seconds.")
            return False
        if confirm.content.lower() != "yes":
            await self.bot.say("Cancelled.")
            return False
        else:
            await self.bot.send_message(self.bot.get_channel('472450201009782787'), embed=transferLog)
            await self.bot.say("Transfer log sent.")

    @commands.command()
    @commands.has_any_role("Tournament Support")
    async def danielAnnouncement(self):
        await self.bot.send_message(self.bot.get_channel('446320268617449493'),
                                    """<@&446374038625976340> <@&446720642478505985> || We've added two new commands to help aid in making roster transactions clearer to see!

The three commands that have been added are simple to use, use them in <#473544946717163540> and they'll ask you a few questions, just answer them and confirm it's correct at the end.

(Commands are cap-sensitive)
To signify the dropping of a player into the free agent pool, use `?playerDrop` 
To signify the acquisition of a player from the free agent pool, use `?freeAgentPickup`
To signify a movement between two teams, use `?playerTrade`

Thank you for your continued interest in OWLET!
- <@222147236728012800>""")

    @commands.command(pass_context=True)
    async def diamondGraduate(self, ctx):
        await self.bot.say("What is the diamond graduates Discord? (Please @ them such as <@" + ctx.message.author.id +
                           ">)")
        discordTag = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)
        if not discordTag:
            await self.bot.say("Timed out.")
            return False
        else:
            servericon = ctx.message.server.icon_url
            embedM = discord.Embed(colour=0x8ce9ff, description="Congrats to " + discordTag.content +
                                                               " on achieving Diamond! <:diamond:474220321562558464> ")
            embedM.set_author(name="OWLET Player Graduate!", icon_url=servericon)
            await self.bot.send_message(self.bot.get_channel('472450201009782787'), embed=embedM)

"""
    async def on_message(self, message):
        author = message.author
        if message.server is None or self.bot.user == author:
            return

        add = discord.User(id='124644921700253696')

        if author != add:
            return
            
        await self.bot.delete_message(message)
"""


def check_folders():
    if not os.path.exists("data/selftosroles"):
        print("Creating data/selftosroles folder...")
        os.makedirs("data/selftosroles")

def check_files():
    if not dataIO.is_valid_json("data/hosting/selftosroles/roles.json"):
        print("Creating emptydata/hosting/selftosroles/roles.json...")
        dataIO.save_json("data/hosting/selftosroles/roles.json", {})

def setup(bot):
    n = SelfToSRoles(bot)
    bot.add_cog(n)     
