from database.db import SqliteDataBase

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