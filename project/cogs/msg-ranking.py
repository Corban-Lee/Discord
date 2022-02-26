import sqlite3
import discord
from discord.ext import commands
from discord.utils import get
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice


class MessageRanking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def database_integrity_check(self):

        # create database table if it doesn't exist
        self.bot.db_utils.create_table(
            table_name='DiscordUsers',
            columns=(
                'id integer PRIMARY KEY',
                'messageCount integer NOT NULL',
                'guildID integer NOT NULL'
            )
        )

        for guild in self.bot.guilds:

            # get list of user ids from database
            guild_users = [row[0] for row in self.bot.db_utils.get_row(
                table_name='DiscordUsers',
                values='"id integer PRIMARY KEY"',
                additional_arg=f'WHERE "guildID integer NOT NULL" LIKE {guild.id}'
            )]

            for user in guild.members:
                if user.id in guild_users:
                    continue

                # insert new row for users that aren't in the list
                self.bot.db_utils.insert_row(
                    table_name='DiscordUsers',
                    values=(user.id, 0, guild.id)
                )


    @commands.Cog.listener()
    async def on_ready(self):
        self.database_integrity_check()
        print('message ranking cog is ready')


    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):

        if message.author.bot:
            return

        try:
            current_message_count = self.bot.db_utils.get_row(
                table_name='DiscordUsers',
                values='*',
                additional_arg=f'WHERE "id integer PRIMARY KEY" LIKE {message.author.id} AND "guildID integer NOT NULL" LIKE {message.guild.id}'
            )[0][1]
            self.bot.db_utils.update_row(
                table_name='DiscordUsers',
                values=f'"messageCount integer NOT NULL" = {current_message_count+1}',
                where=f'"id integer PRIMARY KEY" LIKE {message.author.id} AND "guildID integer NOT NULL" LIKE {message.guild.id}'
            )
        except sqlite3.OperationalError as error:
            print(error)
            self.database_integrity_check()
        
        await self.bot.process_commands(message)

    
    @cog_ext.cog_slash(
        name='Message-Leaderboard',
        description='List of people ranked from most messages to least',
        guild_ids=[819325370087112744, 887853131034157116, 753323563381031042, 810539751143768114],
        options=[
            create_option(
                name='which_server',
                description='Show members from which server?',
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name='This server',
                        value='this'
                    ),
                    create_choice(
                        name='All servers',
                        value='all'
                    )
                ]
            )
        ]
    )
    async def message_leaderboard(self, context:SlashContext, which_server:str):
        await context.defer()
        
        embed = discord.Embed(
            title='Message Leaderboard',
            description='A leaderboard of users ranked from most messages to least'
        )

        # filter down the results to only include members from the guild in the current context
        match which_server:
            case 'this':
                users = self.bot.db_utils.get_row(
                    table_name='DiscordUsers',
                    values='*',
                    additional_arg=f'WHERE "guildID integer NOT NULL" LIKE {context.guild.id}'
                )
                sorted_users = sorted(users, key=lambda x: x[1], reverse=True)
                embed.description += ' from this server.'
                embed.title += f' [{context.guild.name}]'

            case 'all':
                users = self.bot.db_utils.get_row(
                    table_name='DiscordUsers',
                    values='*'
                )
                sorted_users = sorted(users, key=lambda x: x[1], reverse=True)
                embed.description += ' from all of my servers.'
                embed.title += ' [All Servers]'

            case 'combined':
                pass
            # work in progress / / /
            # this should combind scores from all servers

        for i, user_details in enumerate(sorted_users):
            user = get(self.bot.get_all_members(), id=user_details[0])
            guild = get(self.bot.guilds, id=user_details[2])
            value = f'messages: {user_details[1]}' 
            value += f'\nserver: {guild.name}' if which_server != 'this' else ''

            embed.add_field(
                name=f'{i+1}. {user.name}',
                value=value
            )
            if i == 14:
                break

        await context.reply(embed=embed)

    
def setup(bot):
    bot.add_cog(MessageRanking(bot))