from unicodedata import name
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import os


all_cogs = [cog_name[:-3] for cog_name in os.listdir('project/cogs/') if cog_name.endswith('.py')]


class CogTools(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    @commands.Cog.listener()
    async def on_ready():
        print('cog tools is ready')


    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(
        name='Load-Cog',
        description='Load a cog',
        guild_ids=[],
        options=[
            create_option(
                name='cog_name',
                description='What cog do you want to load?',
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name=cog_name.replace('-', ' '),
                        value=cog_name
                    ) for cog_name in all_cogs
                ]
            )
        ]
        
    )
    async def load_cog(self, context:SlashContext, cog_name:str):
        
        try:
            self.bot.load_extension(f'cogs.{cog_name}')
            await context.reply(f'The {cog_name} cog has been loaded successfully')
        except commands.ExtensionAlreadyLoaded:
            await context.reply(f'The {cog_name} cog is already loaded')
        except commands.ExtensionNotFound:
            await context.reply(f'{cog_name} is not a real cog')
        except Exception as e:
            await context.reply(f'I could not load the {cog_name} cog.\n\nError: {e}')

    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(
        name='Unload-Cog',
        description='Unload a cog',
        guild_ids=[],
        options=[
            create_option(
                name='cog_name',
                description='What cog do you want to unload?',
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name=cog_name.replace('-', ' '),
                        value=cog_name
                    ) for cog_name in all_cogs
                ]
            )
        ]
    )
    async def unload_cog(self, context:SlashContext, cog_name:str):

        if cog_name == __file__.split('/')[-1][:-3]:
            await context.reply(f'You cannot unload this cog because it is required to be running for the bot to operate')
            return
        
        try:
            self.bot.unload_extension(f'cogs.{cog_name}')
            await context.reply(f'The {cog_name} cog has been unloaded successfully')
        except commands.ExtensionAlreadyLoaded:
            await context.reply(f'The {cog_name} cog is already unloaded')
        except commands.ExtensionNotFound:
            await context.reply(f'{cog_name} is not a real cog')
        except Exception as e:
            await context.reply(f'I could not unload the {cog_name} cog.\n\nError: {e}')


    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(
        name='Reload-Cog',
        description='Reload a cog',
        guild_ids=[],
        options=[
            create_option(
                name='cog_name',
                description='What cog do you want to Reload?',
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name=cog_name.replace('-', ' '),
                        value=cog_name
                    ) for cog_name in all_cogs
                ]
            )
        ]
    )
    async def reload_cog(self, context:SlashContext, cog_name:str):
        await context.reply(f'Feature is broken because discord-py-slash-commands library is shit')
        # await context.invoke(self.bot.get_command('Unload-Cog'), cog_name=cog_name)
        # await context.invoke(self.bot.get_command('Load-Cog'), cog_name=cog_name)
        # await context.reply(f'I have reload the {cog_name} cog')


    
def setup(bot):
    bot.add_cog(CogTools(bot))