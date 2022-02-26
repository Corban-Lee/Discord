import discord
from discord.ext import commands
from discord_slash import SlashCommand
import sqlite3
import os
import logging
from utils import DatabaseUtility


logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    filename=f'project/logs/logfile-{len(os.listdir("project/logs/"))}.txt',
    format='%(name)s - %(levelname)s - %(message)s',
)

discord_bot = commands.Bot(
    command_prefix='-',
    intents=discord.Intents().all()
)
database = sqlite3.connect('project/db.sqlite3')
discord_bot.db_utils = DatabaseUtility(database)
slash = SlashCommand(discord_bot, sync_commands=True)

# load cogs from project/cogs/ directory
for cog_filename in os.listdir('project/cogs/'):
    if cog_filename.endswith('.py'):
        discord_bot.load_extension(f'cogs.{cog_filename[:-3]}')


@discord_bot.event
async def on_ready():
    print('bot is running')


if __name__ == '__main__':

    # the api key file is not on github. To use this code, you must create your own bot.
    with open('project/apikeys.txt') as file:
        apikey = file.read()
    discord_bot.run(apikey)