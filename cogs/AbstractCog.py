import discord
from discord.ext import commands
import asyncio
class AbstractCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def emojiResponse(self, ctx, title, message, options):
        number_emoji = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        # create embed
        if type(options) is list:
            for i in range(0, len(options)):

                message += "\n"
                message += number_emoji[i] + " - " + options[i]
        embed = discord.Embed(title=title, description=message, colour=discord.Colour.red())
        embed.set_author(name="Bot",
                         icon_url="https://cdn.discordapp.com/avatars/270639428966416385/08816ab4a31d13ed0fd563933dca6536.webp?size=128")

        messageSend = await ctx.send(embed=embed)

        # add reaction
        for number in range(len(options)):
            print(ctx)
            await messageSend.add_reaction(number_emoji[number])
            # await messageSend.add_reaction(ctx.bot.)

        # wait user reaction
        def check(reaction, user):
           return user == ctx.message.author and str(reaction.emoji) in number_emoji

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return None
        else:
            return number_emoji.index(str(reaction.emoji))

    async def textResponse(self, ctx, title, message):
        embed = discord.Embed(title=title, description=message, colour=discord.Colour.red())
        await ctx.send(embed=embed)
        def check(m):
           return m.author == ctx.message.author
        try:
            userMessage = await self.client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return None
        else:
            return userMessage.content