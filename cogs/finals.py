import discord
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
import gspread

maps = {
    "HNMA": "Hanamura",
    "RT66": "Route 66",
    "NEPL": "Nepal",
    "KNRW": "King's Row",
    "VSKA": "Volskaya",
    "WPGB": "WP: Gibraltar",
    "ILOS": "Ilios",
    "NUMB": "Numbani",
    "TOAX": "Temple of Anubis",
    "DRDO": "Dorado",
    "OASX": "Oasis",
    "HLWD": "Hollywood",
    "HOLC": "Horizon Lunar Colony",
    "RIAL": "Rialto",
    "LJTX": "Lijang Tower",
    "BLWR": "Blizzard World",
    "JUNK": "Junkertown",
    "BUSN": "Busan",
    "ECHN": "Eichenwalde",

    "escort": "<:escort:476213138266783764>",
    "2cp": "<:2cp:476213138170183704>",
    "control": "<:control:476213138161795082>",
    "hybrid": "<:hybrid:476213138203607040>"
}


def is_owner():
    def predicate(ctx):
        if ctx.author.id == 222147236728012800:
            return True
        else:
            return False
    return commands.check(predicate)


def has_any_role(*roles):
    def predicate(ctx):
        for role in roles:
            if role in ctx.author.roles():
                return True
            else: continue
        return False
    return commands.check(predicate)


class Finals:
    """OWLETBot Match Embed Poster"""

    def __init__(self, bot):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('data/gsheets/client-secret.json', scope)
        client = gspread.authorize(creds)

        self.sheet = client.open_by_key("1RLYzd6-IaAz1etT-7DlHd8E8yy-sL2nUcsq6Yf5kyIs").worksheet("BotC_F")
        self.bot = bot

    @staticmethod
    def create_embed(row):
        values = row
        ur = 'https://cdn.discordapp.com/icons/443126056766013442/5c15a1c0142553c1e6b794f2d366b5b5.jpg'
        if values[3] == 'QF':
            e = discord.Embed(colour=0x3498DB)
            e.add_field(name='Series Score', value=f'**{values[0]}** {values[29]} - {values[30]} **{values[1]}**')
            e.set_author(name=f'Quarterfinals, {values[2]}', icon_url=ur)
            e.add_field(name='Map Scores',
                        value=f'*{maps[values[4]]}* {maps["escort"]} {values[5]} - {values[6]}\n'
                              f'*{maps[values[7]]}* {maps["control"]} {values[8]} - {values[9]}\n'
                              f'*{maps[values[10]]}* {maps["hybrid"]} {values[11]} - {values[12]}\n'
                              f'*{maps[values[13]]}* {maps["2cp"]} {values[14]} - {values[15]}\n'
                              f'*{maps[values[16]]}* {maps["escort"]} {values[17]} - {values[18]}\n'
                              f'***TB:*** {maps[values[25]]} {maps["control"]} {values[26]} - {values[27]}\n',
                        inline=False)
            return e

        elif values[3] == 'SF':
            e = discord.Embed(colour=0xAF7AC5)
            e.add_field(name='Series Score', value=f'**{values[0]}** {values[29]} - {values[30]} **{values[1]}**')
            e.set_author(name=f'Semifinals, {values[2]}', icon_url=ur)
            e.add_field(name='Map Scores',
                        value=f'*{maps[values[4]]}* {maps["escort"]} {values[5]} - {values[6]}\n'
                              f'*{maps[values[7]]}* {maps["control"]} {values[8]} - {values[9]}\n'
                              f'*{maps[values[10]]}* {maps["hybrid"]} {values[11]} - {values[12]}\n'
                              f'*{maps[values[13]]}* {maps["2cp"]} {values[14]} - {values[15]}\n'
                              f'*{maps[values[16]]}* {maps["escort"]} {values[17]} - {values[18]}\n'
                              f'***TB:*** {maps[values[25]]} {maps["control"]}{values[26]} - {values[27]}\n',
                        inline=False)
            return e

        elif values[3] == 'F':
            e = discord.Embed(colour=0xF7DC6F)
            e.add_field(name='Series Score', value=f'**{values[0]}** {values[29]} - {values[30]} **{values[1]}**')
            e.set_author(name=f'OWLET Grand Finals, {values[2]}', icon_url=ur)
            e.add_field(name='Map Scores',
                        value=f'*{maps[values[4]]}* {maps["control"]} {values[5]} - {values[6]}\n'
                              f'*{maps[values[7]]}* {maps["hybrid"]} {values[8]} - {values[9]}\n'
                              f'*{maps[values[10]]}* {maps["2cp"]} {values[11]} - {values[12]}\n'
                              f'*{maps[values[13]]}* {maps["escort"]} {values[14]} - {values[15]}\n'
                              f'*{maps[values[16]]}* {maps["control"]} {values[17]} - {values[18]}\n'
                              f'*{maps[values[19]]}* {maps["hybrid"]} {values[20]} - {values[21]}\n'
                              f'*{maps[values[22]]}* {maps["escort"]} {values[23]} - {values[24]}\n'
                              f'***TB:*** {maps[values[25]]} {maps["control"]}{values[26]} - {values[27]}\n',
                        inline=False)
            return e
        else:
            return None

    @commands.command(name='finalsEmbeds')
    @is_owner()
    async def finals_embeds(self, num):

        list_of_hashes = self.sheet.get_all_values()

        for row in list_of_hashes:
            if row[3].lower() == num.lower():

                x = self.create_embed(row)

                channel = self.bot.get_channel(476764717369655303)

                m = await channel.send(embed=x)
                try:
                    r = self.sheet.find(row[2]).row
                    self.sheet.update_cell(r, 32, m.id)
                except gspread.exceptions.CellNotFound:
                    pass

    async def match_embed_updater(self):
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(466640219169357835)
        info_channel = self.bot.get_channel(476764717369655303)

        await channel.send('test')

        await asyncio.sleep(10)

        while not self.bot.is_closed():

            list_of_hashes = self.sheet.get_all_values()

            for row in list_of_hashes:
                x = self.create_embed(row)
                try:
                    message = info_channel.get_message(row[31])
                    await message.edit(embed=x)
                except discord.errors.HTTPException:
                    pass
                await asyncio.sleep(2)

            await asyncio.sleep(300)


def setup(bot):
    bot.add_cog(Finals(bot))
    asyncio.get_event_loop().create_task(Finals(bot).match_embed_updater())
