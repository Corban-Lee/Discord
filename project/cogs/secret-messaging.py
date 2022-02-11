import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


class SecretMessaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    @commands.Cog.listener()
    async def on_ready():
        print('secret message cog is ready')


    @cog_ext.cog_slash(
        name='Secret-Message',
        description='Send a secret message to someone through the bot',
        guild_ids=[819325370087112744, 810539751143768114],
        options=[
            create_option(
                name='target',
                description='Who is this message for?',
                option_type=6, # user
                required=True
            ),
            create_option(
                name='message',
                description='What do you want to send?',
                option_type=3,
                required=True
            )
        ]
    )
    async def send_secret_message(self, context:SlashContext, target:discord.Member, message:str):
        try:
            await target.send(f'{message}\n\n*I have been asked to pass on this message discretely by someone in one of your servers.*')
            await context.reply(f'I have sent your message to {target.display_name}', hidden=True)
        except discord.Forbidden:
            await context.reply(f'I cannot send the message to this person. They either have me blocked or I am broken.', hidden=True)


def setup(bot):
    bot.add_cog(SecretMessaging(bot))