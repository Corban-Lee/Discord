import sqlite3
import discord
from discord.ext import commands
from discord.utils import get
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class MessageRanking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def database_integrity_check(self):
        self.bot.db_utils.create_table(
            table_name='DiscordUsers',
            columns=(
                'id integer PRIMARY KEY',
                'messageCount integer NOT NULL',
            )
        )
        all_ids = [row[0] for row in self.bot.db_utils.get_row(
            table_name='DiscordUsers',
            values='*'
        )]
        for guild in self.bot.guilds:
            for user in guild.members:
                if user.id in all_ids:
                    continue

                self.bot.db_utils.insert_row(
                    table_name='DiscordUsers',
                    values=(user.id, 0)
                )
                # prevents the user from being added more than once.
                all_ids.append(user.id)


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
                additional_arg=f'WHERE "id integer PRIMARY KEY" LIKE {message.author.id}'
            )[0][1]
            self.bot.db_utils.update_row(
                table_name='DiscordUsers',
                values=f'"messageCount integer NOT NULL" = {current_message_count+1}',
                where=f'"id integer PRIMARY KEY" LIKE {message.author.id}'
            )
        except sqlite3.OperationalError as error:
            print(error)
            self.database_integrity_check()
        
        await self.bot.process_commands(message)

    
    @cog_ext.cog_slash(
        name='Message-Leaderboard',
        description='List of people ranked from most messages to least',
        guild_ids=[],
    )
    async def message_leaderboard(self, context:SlashContext):
        await context.defer()
        
        embed = discord.Embed(
            title='Message Leaderboard',
            description='A leaderboard of users ranked from most messages to least across every server I am in.'
        )
        users = self.bot.db_utils.get_row(
            table_name='DiscordUsers',
            values='*'
        )
        sorted_users = sorted(users, key=lambda x: x[1], reverse=True)
        for i, user_details in enumerate(sorted_users):
            user = get(self.bot.get_all_members(), id=user_details[0])
            embed.add_field(
                name=f'{i+1}. {user.name}',
                value=f'with {user_details[1]} message(s)'
            )
            if i == 14:
                break

        await context.reply(embed=embed)

    
def setup(bot):
    bot.add_cog(MessageRanking(bot))