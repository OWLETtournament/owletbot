import discord


class ReactRoles:
    """React to a role to get it!"""

    def __init__(self, bot):
        self.bot = bot

    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_user(payload.user_id)

        if payload.message_id == 503226932167704587:
            if payload.emoji.name == 'rowlet':
                role = guild.get_role(503137083418738698)
                await user.add_role(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have added the **Player Applicant** role.',
                                                    colour=discord.Colour.green()))
            elif payload.emoji.name == 'cuteowlet':
                role = guild.get_role(503136885229486083)
                await user.add_role(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have added the **Caster Applicant** role.',
                                                    colour=discord.Colour.green()))
            elif payload.emoji.name == 'scaryowlet':
                role = guild.get_role(503136972886245406)
                await user.add_role(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have added the **Coach Applicant** role.',
                                                    colour=discord.Colour.green()))

    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_user(payload.user_id)

        if payload.message_id == 503226932167704587:
            if payload.emoji.name == 'rowlet':
                role = guild.get_role(503137083418738698)
                await user.remove_role(role, reason='Reaction Roles Removal')
                await user.send(embed=discord.Embed(description='I have removed the **Player Applicant** role.',
                                                    colour=discord.Colour.green()))
            elif payload.emoji.name == 'cuteowlet':
                role = guild.get_role(503136885229486083)
                await user.remove_role(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have removed the **Caster Applicant** role.',
                                                    colour=discord.Colour.green()))
            elif payload.emoji.name == 'scaryowlet':
                role = guild.get_role(503136972886245406)
                await user.remove_role(role, reason='Reaction Roles Addition')
                await user.send(embed=discord.Embed(description='I have removed the **Coach Applicant** role.',
                                                    colour=discord.Colour.green()))


def setup(bot):
    bot.add_cog(ReactRoles(bot))
