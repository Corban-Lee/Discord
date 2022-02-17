from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class Magic8Ball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # check integrity of database for magic 8 ball
        self.database_integrity_check()



    def database_integrity_check(self):
        self.bot.db_utils.create_table(
            table_name='Magic8BallResponses',
            columns=(
                'id integer PRIMARY KEY',
                'content VARCHAR(80) NOT NULL',
                'isPositive BOOL NOT NULL',
            )
        )
        if len(self.bot.db_utils.get_row(
            table_name='Magic8BallResponses',
            values='*'
        )) == 0:
            for id, default in enumerate(
                (
                    ('It is certain', True),
                    ('Without a doubt', True),
                    ('Yes definitely', True),
                    ('You may rely on it', True),
                    ('As I see it, yes', True),
                    ('Most likely', True),
                    ('Outlook good', True),
                    ('Yes', True),
                    ('Reply hazy, try again', False),
                    ('Ask again later', False),
                    ('Better not tell you now', False),
                    ('Cannot predict now', False),
                    ('Concentrate and try again', False),
                    ("Don't count on it", False),
                    ('My reply is no', False),
                    ('My sources say no', False),
                    ('Outlook not so good', False),
                    ('Very doubtful', False),
                )
            ):
                self.bot.db_utils.insert_row(
                    table_name='Magic8BallResponses',
                    values=(id, default[0], default[1])
                )


    @staticmethod
    @commands.Cog.listener()
    async def on_ready():
        print('magic8ball is ready')

    
    @cog_ext.cog_slash(
        name='Magic-8-Ball',
        description='Have your questions answered',
        guild_ids=[],
        options = [
            create_option(
                name='question',
                description='What is your question?',
                option_type=3,
                required=True
            )
        ]
    )
    async def ask_question(self, context:SlashContext, question):
        answer = tuple(self.bot.db_utils.get_row('Magic8BallResponses', '*', additional_arg='ORDER BY RANDOM() LIMIT 18'))[0][1]
        reply = f'*You asked:*   {question}\n*My response is:*   {answer}'
        await context.reply(reply)


    
def setup(bot):
    bot.add_cog(Magic8Ball(bot))