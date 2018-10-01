import discord
from discord.ext import commands
from cogs.utils.HelpPaginator import HelpPaginator, CannotPaginate


class Help:
    """Helpful Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        try:
            if command is None:
                p = await HelpPaginator.from_bot(ctx)
            else:
                entity = self.bot.get_cog(command) or self.bot.get_command(command)

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Command or category "{clean}" not found.')
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int, target: discord.User = None):
        """Purges any amount of messages
        If a user is provided, it will clear only their messages
        If no user is provided, it will clear all of the messages
        You must have Manage Messages permissions to use this command"""

        if number <= 0:
            em = discord.Embed(color=16720640)
            em.add_field(name="Error <:outtick:472572219734884362>", value=f"You must purge at least 1 message!")
            return await ctx.send(embed=em)

        if target is None:
            check = None
        else:
            check = lambda m: m.author == target

        deleted = await ctx.message.channel.purge(limit=number, check=check)

        messages = [f'Deleted __**{len(deleted)}**__ {" message!" if len(deleted) == 1 else " messages!"}']

        embed = discord.Embed(title='Purged <:intick:472572212247920640>', description='\n'.join(messages), color=9305953)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, delete_after=5)


def setup(bot):
    bot.add_cog(Help(bot))
