# -*- coding: UTF-8 -*-

import discord
from data.config import REACTION_MESSAGE_ID
MESSAGE = ("""Hello {0.mention}! Thank you for your interest in joining Owlet. By now, you should have applied for the Coach role by using the Sign Up Form. If you have, rest assured that the admin team will be reviewing your application shortly and will assign you all the necessary roles for you to start your journey with Owlet.

In the meantime, please familiarize yourself with our [official rulebook](https://docs.google.com/document/d/1Qcf3sPA7TqP6jMZVHfTkKmCTVk9n2hgKEz9yGP4RpQw/edit?usp=sharing). It will answer many of your questions, and provide you with a broad-strokes view of the community and tournament values.

Owlet is dedicated to fostering player growth and improvement. That said, the more you put into our tournament, the more you will get out of it. To help you achieve your personal goals and become a successful player in our tournament, we encourage you to adhere to the following guidelines and expectations:
     > Commit to attending matches; Game matches take 1.5 - 2 hours (two per week).
     > Attend team related activities such as practices, scrimmages, map reviews, and vod reviews, which can take 2 - 6+ hours a week (these durations are suggestions only and actual durations will be at your coach’s discretion).
          - During season 1, the typical player committed 4 - 12 hours to Owlet related activities.
     > Be receptive to feedback from your coaches to continuously improve as a player and teammate.
     >Be compliant to all the rules of the Owlet tournament.

As a reminder, if you are applying to the tournament as a free agent, you must take it upon yourself to seek a team through tryouts, networking and engagement with your fellow Owlets.

Thanks again for your interest in the Owlet Community Tournament! If you have any questions, please message the <@447612665947357185> bot in the Owlet server. We look forward to seeing you take flight with us!""")


class ReactRoles:
    """React to a role to get it!"""

    def __init__(self, bot):
        self.bot = bot

    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        if payload.message_id == REACTION_MESSAGE_ID:
            if payload.emoji.name == 'rowlet':
                role = guild.get_role(503137083418738698)
                em = discord.Embed(colour=discord.Colour.orange())
                em.description = MESSAGE.format(ctx.author)
    
                await user.send(file=discord.File('w2o.png', filename='welcome.png'))
                await user.send(embed=em)
                await user.add_roles(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have added the **Player Applicant** role.',
                                                    colour=discord.Colour.green()))
            elif payload.emoji.name == 'cuteowlet':
                role = guild.get_role(503136885229486083)
                await user.add_roles(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have added the **Caster Applicant** role.',
                                                    colour=discord.Colour.green()))
            elif payload.emoji.name == 'scaryowlet':
                role = guild.get_role(503136972886245406)
                await user.add_roles(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have added the **Coach Applicant** role.',
                                                    colour=discord.Colour.green()))

    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        if payload.message_id == REACTION_MESSAGE_ID:
            if payload.emoji.name == 'rowlet':
                role = guild.get_role(503137083418738698)
                await user.remove_roles(role, reason='Reaction Roles Removal')
                await user.send(embed=discord.Embed(description='I have removed the **Player Applicant** role.',
                                                    colour=discord.Colour.red()))
            elif payload.emoji.name == 'cuteowlet':
                role = guild.get_role(503136885229486083)
                await user.remove_roles(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have removed the **Caster Applicant** role.',
                                                    colour=discord.Colour.red()))
            elif payload.emoji.name == 'scaryowlet':
                role = guild.get_role(503136972886245406)
                await user.remove_roles(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have removed the **Coach Applicant** role.',
                                                    colour=discord.Colour.red()))


def setup(bot):
    bot.add_cog(ReactRoles(bot))

