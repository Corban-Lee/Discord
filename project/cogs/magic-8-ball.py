from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class Magic8Ball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    @commands.Cog.listener()
    async def on_ready():
        print('magic8ball is ready')

    
    @cog_ext.cog_slash(
        name='Magic-8-Ball',
        description='Have your questions answered',
        guild_ids=[819325370087112744],
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
        answer = tuple(self.bot.db_utils.get('Magic8BallResponses', '*', 'RANDOM() LIMIT 18'))[0][1]
        reply = f'You asked: {question}\nMy response is: {answer}'
        await context.reply(reply)


    
def setup(bot):
    bot.add_cog(Magic8Ball(bot))