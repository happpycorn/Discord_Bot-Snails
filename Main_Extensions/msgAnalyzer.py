from discord.ext import commands
from Database.db import SqliteDataBase

class MsgAnalyzer(commands.Cog):

    # Init : Bot and Database
    def __init__(self, bot) -> None:

        self.bot = bot
        self.message_database = SqliteDataBase()

async def setup(bot) : await bot.add_cog(MsgAnalyzer(bot))