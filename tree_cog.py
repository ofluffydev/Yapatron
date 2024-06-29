from discord.ext import commands


class TreeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(self.bot.GUILD_ID)
        if guild is None:
            print(f'Guild with ID {self.bot.GUILD_ID} not found!')
            exit(1)
        else:
            print(f'Connected to guild: {guild.name}')

        @self.tree.command(name="first_command", description="My first application Command", guild=guild)
        async def first_command(interaction):
            await interaction.response.send_message("Hello!")

        print('Loaded tree commands')

        print('About to sync tree')
        try:
            await self.bot.tree.sync()
        except Exception as e:
            print(f'Error while syncing tree: {e}')
        else:
            print('Tree synced')


async def setup(bot):
    await bot.add_cog(TreeCog(bot))
