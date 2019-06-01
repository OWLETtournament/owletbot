import asyncio
import json
from datetime import datetime, timedelta

from discord.ext import commands


class ModmailChecker:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="creatediscussion")
    async def create_discussion(self, ctx, discussion_name, *, discussion_description):
        """
        Creates a discussion.
    
        Takes in 2 parameters: a discussion name (MUST BE NO SPACES!!!!), and a discussion description.
        """
        discussion_cat = ctx.guild.get_channel(465948052025507860)
        c = await ctx.guild.create_text_channel(discussion_name, category=discussion_cat, topic=discussion_description)
        await ctx.send(f"Channel {c.mention} created successfully!")
            

def setup(bot):
    bot.add_cog(ModmailChecker(bot))
