import discord
import pandas as pd
from wordcloud import WordCloud
from discord.ext import commands
from Database.db import SqliteDataBase

class CommandExtension(commands.Cog):

    @commands.command()
    async def draw_word_cloud(self, ctx) -> None:

        await ctx.send("waiting...")

        conn, _ = self.message_database.connect_to_db()

        text = pd.read_sql_query(
            """
            SELECT content FROM messages
            WHERE timestamp >= DATE('now', '-7 days')
            """, conn)

        text = ' '.join(text['content'].dropna())

        wordcloud = WordCloud(
            font_path=r"Asset\IBMPlexSansTC-Light.ttf",
            width=4096, height=2160, colormap='Blues',
            background_color="white",
            mode='RGBA'
        ).generate(text)

        wordcloud.to_file(r"Asset\wordCloud.png")

        await ctx.send(file=discord.File(r"Asset\wordCloud.png"))
    
    def __init__(self, bot):
        
        self.bot = bot
        self.message_database = SqliteDataBase()

def setup(bot) : bot.add_cog(CommandExtension(bot))