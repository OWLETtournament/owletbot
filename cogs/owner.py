# -*- coding: UTF-8 -*-

from discord.ext import commands
import traceback
import discord
import textwrap
from contextlib import redirect_stdout
import io
from platform import python_version
import copy

# For the eval command

import os
import sys


class Owner:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    @staticmethod
    def cleanup_code(content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @commands.command(hidden=True, name='eval', aliases=['evaluate'])
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a piece of code"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        # iOS Form
        body = body.replace("“", '"')
        body = body.replace("”", '"')
        body = body.replace("‘", "'")
        body = body.replace("’", "'")

        icon = "http://i.imgur.com/9EftiVK.png"

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            fooem = discord.Embed(color=0xff0000)
            fooem.add_field(name="Code evaluation was not successful. <:peposad:496434027897552896>", value=f'```\n{e.__class__.__name__}: {e}\n```'
                            .replace(self.bot.http.token, '•' * len(self.bot.http.token)))
            fooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url=icon)
            fooem.timestamp = ctx.message.created_at
            return await ctx.send(embed=fooem)

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            fooem = discord.Embed(color=0xff0000)
            fooem.add_field(name="Code evaluation was not successful. <:peposad:496434027897552896>", value=f'```py\n{value}{traceback.format_exc()}'
                                                                              f'\n```'.replace(self.bot.http.token,
                                                                                               '•' * len(self.bot.http.token)))
            fooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url=icon)
            fooem.timestamp = ctx.message.created_at
            await ctx.send(embed=fooem)
        else:
            value = stdout.getvalue()

            try:
                await ctx.message.add_reaction(':white_check_mark:')
            except:
                pass

            if ret is None:
                if value:
                    sfooem = discord.Embed(color=discord.Colour.green())
                    sfooem.add_field(name="Code evaluation was successful! <:hypers:496434027348230177>", value=f'```py\n{value}\n```'.
                                     replace(self.bot.http.token, '•' * len(self.bot.http.token)))
                    sfooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url=icon)
                    sfooem.timestamp = ctx.message.created_at
                    await ctx.send(embed=sfooem)
            else:
                self._last_result = ret
                ssfooem = discord.Embed(color=discord.Colour.green())
                ssfooem.add_field(name="Code evaluation was successful! <:hypers:496434027348230177>", value=f'```py\n{value}{ret}\n```'
                                  .replace(self.bot.http.token, '•' * len(self.bot.http.token)))
                ssfooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url=icon)
                ssfooem.timestamp = ctx.message.created_at
                await ctx.send(embed=ssfooem)

    @commands.command(hidden=True, aliases=["say", "print"])
    @commands.is_owner()
    async def echo(self, ctx, *, content):
        await ctx.send(content)

    @commands.command(hidden=True, aliases=["impersonate"])
    @commands.is_owner()
    async def runas(self, ctx, member: discord.Member, *, cmd):
        """Invoke bot command as specified user"""
        msg = copy.copy(ctx.message)
        msg.content = f"{ctx.me.mention} {cmd}"
        msg.author = member
        await self.bot.process_commands(msg)

    @commands.command(hidden=True, aliases=['die', 'kys', 'neckrope'])
    @commands.is_owner()
    async def restart(self, ctx):
        """Restarts the bot"""
        await ctx.send(embed=discord.Embed(color=0x00FFFF, description="wow lowkey rude but fine"))
        os.execl(sys.executable, sys.executable, * sys.argv)


def setup(bot):
    bot.add_cog(Owner(bot))
    print('Owner module loaded.')
