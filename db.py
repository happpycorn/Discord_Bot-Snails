import discord
import sqlite3
import pandas as pd
from wordcloud import WordCloud
from datetime import datetime

class SqliteDataBase:

    # 初始化資料庫
    def __init__(self) -> None:

        self.db_paths = {
            'public': 'public_messages.db',
            'member': 'member_messages.db',
            'staff': 'staff_messages.db'
        }

    # 連接資料庫
    def connect_to_db(self, db_path) -> tuple:

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # 讓結果以字典格式返回 ***

        return (conn, conn.cursor())

class MessageCatcher(SqliteDataBase):

    channel_permission = {
        '1139183046818545794' : 'public',
        '1160152151167860786' : 'member'
    }

    def __init__(self) -> None:

        super().__init__()

        # 初始化資料庫
        for db_path in self.db_paths.values():

            conn, cursor = self.connect_to_db(db_path)

            # 資料庫結構 : 訊息 ID, 文字內容, 發送者, 頻道, 類別, 時間
            cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                        (message_id INTEGER PRIMARY KEY, content TEXT, author TEXT, channel TEXT, category TEXT, timestamp TEXT)''')
            
            conn.commit()
            conn.close()
    
    # 加入訊息
    async def add_message(self, message) -> None:
        
        print(f"Received message: {message.content} from {message.author}")

        db_path = self.get_db_path(message)

        conn, cursor = self.connect_to_db(db_path)

        cursor.execute('INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?, ?)', 
        (message.id, message.content, str(message.author), str(message.channel), str(message.channel.category.id), str(message.created_at)))

        conn.commit()
        conn.close()

    # 回傳合適的路徑
    def get_db_path(self, message):

        # 取得類別
        category = message.channel.category

        # 判斷有沒有在 id 中
        if category and str(category.id) in self.channel_permission.keys():

            key = self.channel_permission[str(category.id)]
            return self.db_paths.get(key, self.db_paths['staff'])
        
        # 沒有的話回傳 staff
        return self.db_paths['staff']

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
            font_path="asset\IBMPlexSansTC-Light.ttf",
            width=4096, height=2160, colormap='Blues',
            background_color="white",
            mode='RGBA'
            ).generate(text)

        wordcloud.to_file("asset\wordcloud.png")

        await ctx.send(file=discord.File("asset\wordcloud.png"))