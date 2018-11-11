import discord

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


class Welcomer:
  """Gives welcomes!"""
  
  async def on_member_join(self, member):
    em = discord.Embed(colour=discord.Colour.orange())
    em.description = MESSAGE.format(member)
    
    await ctx.send(file=discord.File('w2o.png', filename='welcome.png'))
    await ctx.send(embed=em)
    
def setup(bot):
  bot.load_extension(Welcomer(bot))
    
