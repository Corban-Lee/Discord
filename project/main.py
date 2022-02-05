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
                self.load_extension(f'cogs.{cogfile[:-3]}')


        # _list = [
        #     'Reply hazy, try again',
        #     'Ask again later',
        #     'Better not tell you now',
        #     'Cannot predict now',
        #     'Concentrate and ask again',
        #     "Don't count on it",
        #     'My reply is no',
        #     'My sources say no',
        #     'Outlook not so good',
        #     'Very doubtful'
        # ]

        # for id, item in enumerate(_list):

        #     id += 9

        #     self.db_insert(
        #         'Magic8BallResponses', 
        #         (
        #             id,
        #             item,
        #             False
        #         )
        #     )


    @staticmethod
    async def on_ready():
        print('bot is running')


    # database related methods - - - - - - - - - -


    def db_action(self, action:str):
        cur = self.db.cursor()
        print(action)
        execution = cur.execute(action)
        self.db.commit()
        return execution


    def db_create_table(self, table_name:str, columns:tuple):
        self.db_action(f'CREATE TABLE {table_name} {columns}')
        


    def db_insert(self, table_name:str, values:tuple):
        self.db_action(f'INSERT INTO {table_name} VALUES {values}')



    def db_retrieve(self, table_name:str, values:tuple, orderby:tuple=None) -> tuple:
        if orderby:
            return self.db_action(f'SELECT {values} FROM {table_name} ORDER BY {orderby}')
        return self.db_action(f'SELECT {values} FROM {table_name}')


if __name__ == '__main__':

    # the api key file is not on github. To use this code, you must create your own bot.
    with open('project/apikeys.txt') as file:
        apikey = file.read()
    DiscordBot().run(apikey)