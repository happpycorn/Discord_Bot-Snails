import sqlite3
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd

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

    data_types = {
        'channel' : """
        SELECT channel, COUNT(*) as message_count
        FROM messages
        GROUP BY channel
        ORDER BY message_count DESC
        LIMIT 3;
        """
    }

    def __init__(self) -> None:

        super().__init__('messages.db')

    async def data_send(self, ctx, datatype : str) -> None:

        conn, _ = self.connect_to_db()

        df = pd.read_sql_query(self.data_types[datatype], conn)

        await ctx.send(df)