import discord
import dotenv
import os
import glob
from discord.ext import commands

dotenv.load_dotenv()


bot = commands.Bot(command_prefix='$', description="This is a Helper Bot")
commandRelPath="./cogs/commands/"

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir(commandRelPath):
    if filename.endswith('.py'):
        commandModulePath = commandRelPath[2:].rstrip('/').replace('/', '.')
        bot.load_extension(f'{commandModulePath}.{filename[:-3]}')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# @bot.event
# async def on_reaction_add(reaction, user):
#     channel = reaction.message.channel
#     await bot.(channel, "{}".format(reaction.emoji))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


bot.run(os.getenv('CLIENT_TOKEN'))

# to start the bot :
# py -3 example_bot.py
