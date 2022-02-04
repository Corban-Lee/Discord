import discord
from discord.ext import commands
from discord_slash import SlashCommand
import sqlite3
import os


class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='-',
            intents=discord.Intents().all()
        )
        self.slash = SlashCommand(self, sync_commands=True)
        self.db = sqlite3.connect('project/db.sqlite3')

        # load cogs from project/cogs/ directory
        for cogfile in os.listdir('project/cogs/'):
            if cogfile.endswith('.py'):
                self.load_extension(f'project.cogs.{cogfile[:-3]}')


    @staticmethod
    async def on_ready():
        print('bot is running')


    # database related methods - - - - - - - - - -
    #
    # this might not be good way of doing things. If two different tasks need to be completed
    # then the db will be opened and closed twice instead of once.


    def db_action(self, action:str):
        cur = self.db.cursor()
        cur.execute(action)
        cur.commit()
        cur.close()


    def db_create_table(self, table_name:str, columns:tuple):
        self.db_action(f'CREATE TABLE {table_name} {columns}')
        


    def db_insert(self, table_name:str, values:tuple):
        self.db_action(f'INSERT INTO {table_name} VALUES {values}')



    def db_retrieve(self, table_name:str, values:tuple, orderby:tuple) -> tuple:
        return self.db_action(f'SELECT {values} FROM {table_name} ORDER BY {orderby}')


if __name__ == '__main__':

    # the api key file is not on github. To use this code, you must create your own bot.
    with open('project/apikeys.txt') as file:
        apikey = file.read()
    DiscordBot().run(apikey)