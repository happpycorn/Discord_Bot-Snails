import discord
import pandas as pd
from datetime import datetime
from wordcloud import WordCloud
from database.db import SqliteDataBase

class MessageAnlyzer(SqliteDataBase):

    def __init__(self) -> None:

        super().__init__()

    # 尋找說最多話的頻道
    async def popular_channel(self, ctx, db_path=None) -> None:

        if db_path is None: db_path = self.db_paths['public']

        conn, _ = self.connect_to_db(db_path)

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

        description = f"""

        #1 | {df.iloc[0]['message_count']:<6} | {df.iloc[0]['channel']}
        """

        if len(df) > 2:

            description += f"""

            #2 | {df.iloc[1]['message_count']:<6} | {df.iloc[1]['channel']}
            """

        if len(df) > 3:

            description += f"""

            #3 | {df.iloc[2]['message_count']:<6} | {df.iloc[2]['channel']}
            """

        embed = discord.Embed(
            title="Top Channels by Message Count in the Past Week",
            description=description,
            timestamp=datetime.utcnow(),
            color=discord.Color.blue()
        )

        # Send the embed with the data
        await ctx.send(embed=embed)
    
    # 繪製文字雲
    async def draw_word_cloud(self, ctx, db_path=None) -> None:

        await ctx.send("waiting...")

        if db_path is None: db_path = self.db_paths['public']

        conn, _ = self.connect_to_db(db_path)

        text = pd.read_sql_query(
            """
            SELECT content FROM messages
            WHERE timestamp >= DATE('now', '-7 days')
            """, conn)

        text = text = ' '.join(text['content'].dropna())

        wordcloud = WordCloud(
            font_path="asset\\IBMPlexSansTC-Light.ttf",
            width=4096, height=2160, colormap='Blues',
            background_color="white",
            mode='RGBA'
            ).generate(text)

        wordcloud.to_file("asset\\wordcloud.png")

        await ctx.send(file=discord.File("asset\\wordcloud.png"))
