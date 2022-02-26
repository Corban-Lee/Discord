import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice


class MemberTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    @commands.Cog.listener()
    async def on_ready():
        print('member tools cog is ready')


    @commands.has_permissions(administrator=True)
    @cog_ext.cog_slash(
        name='Edit-Nicknames',
        description='Edit nicknames of all server members',
        guild_ids=[819325370087112744, 887853131034157116, 912068802005569557],
        options=[
            create_option(
                name='edit',
                description='Edit what part of the nickname?',
                option_type=4,
                required=True,
                choices=[
                    create_choice(
                        name='Prefix',
                        value=1
                    ),
                    create_choice(
                        name='Suffix',
                        value=2
                    ),
                    create_choice(
                        name='Entire Nickname',
                        value=3
                    )
                ]
            ),
            create_option(
                name='change',
                description='What will the new nickname be',
                option_type=3,
                required=True,
            )
        ]
    )
    async def edit_nicknames(self, context:SlashContext, edit:int, change:str):
        """Changes all nicknames in a server
        :param edit: The part of the nickname to edit. Must be 1, 2 or 3 (Prefix, Suffix and Entire nickname respectively).
        :param change: The new string of characters to replace or be appended onto the previous nickname.
        """

        if edit == 1:
            new_nickname = lambda old, change: f'{change}{old}'
        elif edit == 2:
            new_nickname = lambda old, change: f'{old}{change}'
        else:
            new_nickname = lambda old, change: f'{change}'

        # not using enumerate because some times there should be no increment
        count = 0
        for user in context.guild.members:
            try:
                old = user.nick if user.nick is not None else user.name
                await user.edit(nick=new_nickname(old, change))
                count += 1
                
            except discord.Forbidden:
                pass

            except discord.NotFound:
                pass

            except discord.HTTPException:
                pass

        await context.reply(f'I have updated {count} user nicknames')


def setup(bot):
    bot.add_cog(MemberTools(bot))