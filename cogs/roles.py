# -*- coding: UTF-8 -*-

import discord
from discord.ext import commands
import asyncio


class Roles:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def roles(self, ctx):

        if ctx.channel.id not in [466640219169357835, 449660180989345802]:
            await self.bot.say('You cannot use this command in a non bot-spam channel.')
            return

        owlet = self.bot.get_guild(443126056766013442)

        # TZ Roles
        est = owlet.get_role(449634029956759572)
        cst = owlet.get_role(449634099821412362)
        mst = owlet.get_role(449634157169999882)
        pst = owlet.get_role(449634200631640064)

        # Region Roles
        na = owlet.get_role(449633759353110541)
        eu = owlet.get_role(449633899631607809)

        # Applicant Roles
        player = owlet.get_role(482254224252469260)
        coach = owlet.get_role(482254235480752128)
        caster = owlet.get_role(482254237548544000)
        ref = owlet.get_role(481104680953315331)

        author = ctx.author

        categ_em = discord.Embed(colour=0xF7DC6F, description="⏱ - Timezone\n"
                                                              "🌎 - Region\n"
                                                              "📝 - Applicant Roles\n\n"
                                                              "❌ - Cancel and exit")
        categ_em.set_author(name="Role-Assign Menu Category Picker")

        categs = await ctx.send(embed=categ_em)

        def check(reaction, user):
            return user == ctx.message.author and \
                   str(reaction.emoji) in ['⏱', '🌎', '📝', '❌', '🏙', '🌲', '🌵', '🎥', '❌', '🇺🇸', '🇪🇺', '❌']

        categ_react, user = self.bot.loop.create_task(self.bot.wait_for('reaction_add', check=check, timeout=60))
        await categs.add_reaction('⏱')
        await categs.add_reaction('🌎')
        await categs.add_reaction('📝')
        await categs.add_reaction('❌')

        if categ_react.emoji == '⏱':  # If TZ selected
            await categs.delete()

            tz_em = discord.Embed(colour=0x7FB3D5, description="🏙️ - EST/EDT\n"
                                                               "🌲 - CST/CDT\n"
                                                               "🌵 - MST/MDT\n"
                                                               "🎥 - PST/PDT\n\n"
                                                               "❌ - Cancel and exit""")
            tz_em.set_author(name='Timezone-Assign Select Menu')

            tz_message = await ctx.send(embed=tz_em)

            tz_react, user = self.bot.loop.create_task(self.bot.wait_for('reaction_add', check=check, timeout=60))

            await tz_message.add_reaction('🏙')
            await tz_message.add_reaction('🌲')
            await tz_message.add_reaction('🌵')
            await tz_message.add_reaction('🎥')
            await tz_message.add_reaction('❌')

            if tz_react.emoji == '🏙':  # EST
                await tz_message.delete()
                await author.add_roles(est, reason='Auto-role Menu Assign')
                await asyncio.sleep(1)
                if cst in author.roles:
                    await author.remove_roles(cst, reason='Auto-role Menu Assign')
                elif mst in author.roles:
                    await author.remove_roles(mst, reason='Auto-role Menu Assign')
                elif pst in author.roles:
                    await author.remove_roles(pst, reason='Auto-role Menu Assign')
                await ctx.send(embed=discord.Embed(description='Roles successfully added.', colour=0xAED6F1))
                return

            elif tz_react.emoji == '🌲':  # CST
                await tz_message.delete()
                await author.add_roles(cst, reason='Auto-role Menu Assign')
                await asyncio.sleep(1)
                if est in author.roles:
                    await author.remove_roles(est, reason='Auto-role Menu Assign')
                elif mst in author.roles:
                    await author.remove_roles(mst, reason='Auto-role Menu Assign')
                elif pst in author.roles:
                    await author.remove_roles(pst, reason='Auto-role Menu Assign')
                await ctx.send(embed=discord.Embed(description='Roles successfully added.', colour=0xAED6F1))
                return

            elif tz_react.emoji == '🌵':  # MST
                tz_message.delete()
                await author.add_roles(mst, reason='Auto-role Menu Assign')
                await asyncio.sleep(1)
                if est in author.roles:
                    await author.remove_roles(est, reason='Auto-role Menu Assign')
                elif cst in author.roles:
                    await author.remove_roles(cst, reason='Auto-role Menu Assign')
                elif pst in author.roles:
                    await author.remove_roles(pst, reason='Auto-role Menu Assign')
                await ctx.send(embed=discord.Embed(description='Roles successfully added.', colour=0xAED6F1))
                return

            elif tz_react.emoji == '🎥':  # PST
                await tz_message.delete()
                await author.add_roles(pst, reason='Auto-role Menu Assign')
                await asyncio.sleep(1)
                if est in author.roles:
                    await author.remove_roles(est, reason='Auto-role Menu Assign')
                elif cst in author.roles:
                    await author.remove_roles(cst, reason='Auto-role Menu Assign')
                elif mst in author.roles:
                    await author.remove_roles(mst, reason='Auto-role Menu Assign')
                await ctx.send(embed=discord.Embed(description='Roles successfully added.', colour=0xAED6F1))
                return

            elif tz_react.emoji == '❌':  # Cancelled command
                await tz_message.delete()
                await ctx.send(embed=discord.Embed(description='Command cancelled.', colour=0xAED6F1))
                return

            else:  # No react within 60s
                await tz_message.delete()
                await ctx.send(embed=discord.Embed(description='Timed out.', colour=0xAED6F1))
                return

        elif categ_react.emoji == '🌎':  # If region roles selected
            await categs.delete()
            region_embed = discord.Embed(description="🇺🇸 - NA\n"
                                                     "🇪🇺 - EU\n\n"
                                                     "❌ - Cancel and exit", colour=0xF5B7B1)
            region_embed.set_author(name='Region-Assign Select Menu')

            region_message = await ctx.send(embed=region_embed)
            
            region_react, user = self.bot.loop.create_task(self.bot.wait_for('reaction_add', check=check, timeout=60))

            await region_message.add_reaction('🇺🇸')
            await region_message.add_reaction('🇪🇺')
            await region_message.add_reaction('❌')

            if region_react.emoji == '🇺🇸':  # If NA selected
                await region_message.delete()
                await author.add_roles(na, reason='Auto-role Menu Assign')
                await asyncio.sleep(1)
                if eu in author.roles:
                    await author.remove_roles(eu, reason='Auto-role Menu Assign')
                    pass
                await ctx.send(embed=discord.Embed(description='Role successfully added.', colour=0xAED6F1))
                return

            elif region_react.emoji == '🇪🇺':  # If EU selected
                await region_message.delete()
                await author.add_roles(eu, reason='Auto-role Menu Assign')
                await asyncio.sleep(1)
                if na in author.roles:
                    await author.remove_roles(na, reason='Auto-role Menu Assign')
                await ctx.send(embed=discord.Embed(description='Role successfully added.', colour=0xAED6F1))
                return

            elif region_react.emoji == '❌':  # If cancelled
                await region_message.delete()
                await ctx.send(embed=discord.Embed(description='Cancelled.', colour=0xAED6F1))
                return

            else:  # If no react after 60s
                await region_message.delete()
                await ctx.send(embed=discord.Embed(description='Timed out.', colour=0xAED6F1))

        elif categ_react.emoji == '📝':  # Applicant reactions
            await categs.delete()
            applicant_embed = discord.Embed(colour=0xD2B4DE, description="🖥️ - Player Applicant\n"
                                                                         "🎥 - Caster Applicant\n"
                                                                         "🏁 - Referee Applicant\n"
                                                                         "🎓 - Coach Applicant\n\n"
                                                                         "❌ - Cancel and exit")
            applicant_embed.set_author(name='Applicant-Assign Select Menu')

            applicant = await ctx.send(ctx.message.channel, embed=applicant_embed)

            applicant_react, user = self.bot.loop.create_task(self.bot.wait_for('reaction_add', check=check, timeout=60))

            await applicant.add_reaction('💻')
            await applicant.add_reaction('🎥')
            await applicant.add_reaction('🏁')
            await applicant.add_reaction('🎓')
            await applicant.add_reaction('❌')

            removed_role_em = discord.Embed(description='Role successfully removed.', colour=0xEC7063)
            added_role_em = discord.Embed(description='Role successfully added.', colour=0x1ABC9C)

            if applicant_react.emoji == '💻':
                await applicant.delete_message()
                await asyncio.sleep(1)
                if player in author.roles:
                    await author.remove_roles(player, reason='Auto-role Self Assign')
                    await ctx.send(embed=removed_role_em)
                    return
                elif player not in author.roles:
                    await author.remove_roles(player, reason='Auto-role Self Assign')
                    await ctx.send(embed=added_role_em)
                    return
            elif applicant_react.emoji == '🎥':
                await applicant.delete()
                if caster in author.roles:
                    await author.remove_roles(caster, reason='Auto-role Self Assign')
                    await ctx.send(embed=removed_role_em)
                    return
                elif caster not in author.roles:
                    await author.add_roles(caster, reason='Auto-role Self Assign')
                    await ctx.send(embed=added_role_em)
                    return
            elif applicant_react.emoji == '🏁':
                await applicant.delete()
                if ref in author.roles:
                    await author.remove_roles(ref, reason='Auto-role Self Assign')
                    await ctx.send(embed=removed_role_em)
                    return
                elif ref not in author.roles:
                    await author.add_roles(ref, reason='Auto-role Self Assign')
                    await ctx.send(embed=added_role_em)
                    return
            elif applicant_react.emoji == '🎓':
                await applicant.delete()
                if coach in author.roles:
                    await author.remove_roles(coach, reason='Auto-role Self Assign')
                    await ctx.send(embed=removed_role_em)
                    return
                elif coach not in author.roles:
                    await author.add_roles(coach, reason='Auto-role Self Assign')
                    await ctx.send(embed=added_role_em)
                    return
            elif applicant_react.emoji == '❌':
                await applicant.delete()
                await ctx.send(embed=discord.Embed(description='Cancelled.', colour=0xAED6F1))
            else:
                await applicant.delete()
                await ctx.send(embed=discord.Embed(description='Timed out.', colour=0xAED6F1))

        elif categ_react.emoji == '❌':
            await categs.delete()
            await ctx.send(embed=discord.Embed(description='Cancelled.', colour=0xAED6F1))
            return

        elif categ_react is None:
            await categs.delete()
            await ctx.send(embed=discord.Embed(description="Timed out.", colour=0xAED6F1))
            return


def setup(bot):
    bot.add_cog(Roles(bot))
