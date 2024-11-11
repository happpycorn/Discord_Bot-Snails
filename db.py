import discord
import sqlite3
import pandas as pd
from tqdm import tqdm
from wordcloud import WordCloud
from datetime import datetime, timedelta

class SqliteDataBase:

    # 初始化資料庫
    def __init__(self, db_path) -> None:

        self.db_path = db_path

    # 連接資料庫
    def connect_to_db(self):

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 讓結果以字典格式返回 ***

        return (conn, conn.cursor())

class MessageManager(SqliteDataBase):

    black_list = [
        "小蝸#0685",
        "YEE式機器龍#9027"
    ]

    def __init__(self) -> None:

        super().__init__('messages.db')

        # 初始化資料庫

        conn, cursor = self.connect_to_db()

        # 資料庫結構 : 訊息 ID, 文字內容, 發送者, 頻道, 時間
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                    (message_id INTEGER PRIMARY KEY, content TEXT, author TEXT, channel TEXT, timestamp TEXT)''')
        
        conn.commit()
        conn.close()
    
    async def add_message(self, message) -> None:

        conn, cursor = self.connect_to_db()

        cursor.execute('INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?)', 
        (message.id, message.content, str(message.author), str(message.channel), str(message.created_at)))

        conn.commit()
        conn.close()

    # 不使用
    async def fetch_recent_messages(self, ctx) -> None:

        await ctx.send('Fetching messages from the past week...')
    
        one_week_ago = datetime.now() - timedelta(days=7)
        conn, cursor = self.connect_to_db()
        cursor.execute("DELETE FROM messages")
        
        # 抓取近一週的訊息
        for channel in tqdm(ctx.guild.text_channels):
            async for message in channel.history(limit=None, after=one_week_ago):

                if str(message.author) in self.black_list:
                    continue

                # 將訊息存入資料庫
                cursor.execute('INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?)', 
                        (message.id, message.content, str(message.author), str(message.channel), str(message.created_at)))
    
        conn.commit()
        conn.close()

        await ctx.send('Recent messages from the past week have been fetched and saved to the database.')

class MessageAnlyzer(SqliteDataBase):

    def __init__(self) -> None:

        super().__init__('messages.db')

    async def popular_channel(self, ctx) -> None:

        conn, _ = self.connect_to_db()

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

        embed = discord.Embed(
            title="Top Channels by Message Count in the Past Week",
            description=
            f"""

            #1 | {df.iloc[0]['message_count']:<6} | {df.iloc[0]['channel']}

            #2 | {df.iloc[1]['message_count']:<6} | {df.iloc[1]['channel']}

            #3 | {df.iloc[2]['message_count']:<6} | {df.iloc[2]['channel']}
            """,
            timestamp=datetime.utcnow(),
            color=discord.Color.blue()
        )

        # Send the embed with the data
        await ctx.send(embed=embed)
    
    async def draw_word_cloud(self, ctx) -> None:

        await ctx.send("waiting...")

        conn, _ = self.connect_to_db()

        text = pd.read_sql_query(
            """
            SELECT content FROM messages
            WHERE timestamp >= DATE('now', '-7 days')
            """, conn)

        text = text = ' '.join(text['content'].dropna())

        wordcloud = WordCloud(
            font_path="asset\IBMPlexSansTC-Light.ttf",
            width=4096, height=2160, colormap='Blues',
            background_color="white",
            mode='RGBA'
            ).generate(text)

        wordcloud.to_file("asset\wordcloud.png")

        await ctx.send(file=discord.File("asset\wordcloud.png"))