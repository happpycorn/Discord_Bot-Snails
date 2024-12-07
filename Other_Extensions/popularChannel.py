import discord
import pandas as pd
from datetime import datetime
from discord.ext import commands

import sys
sys.path.append("..")
from Database.db import SqliteDataBase

class CommandExtension(commands.Cog):

    # Find Popular Channel
    @commands.command()
    async def popularChannel(self, ctx) -> None:

        # Get Data
        conn, _ = self.message_database.connect_to_db()

        df = pd.read_sql_query(
            """
            SELECT channel, COUNT(*) as message_count
            FROM messages
            WHERE timestamp >= DATE('now', '-7 days')
            GROUP BY channel
            ORDER BY message_count DESC
            LIMIT 3;
            """, conn)

        if df.empty:
            await ctx.send("No data available.")
            return
        
        # Creat Embed
        description = ""

        for i in range(len(df)):

            description += f"""

            #{i+1} | {df.iloc[i]['message_count']:<6} | {df.iloc[i]['channel']}
            """

        embed = discord.Embed(
            title="Top Channels by Message Count in the Past Week",
            description=description,
            timestamp=datetime.utcnow(),
            color=discord.Color.blue()
        )

        # Send the embed with the data
        await ctx.send(embed=embed)
    
    # Init
    def __init__(self, bot):
        
        self.bot = bot
        self.message_database = SqliteDataBase()

def setup(bot) : bot.add_cog(CommandExtension(bot))