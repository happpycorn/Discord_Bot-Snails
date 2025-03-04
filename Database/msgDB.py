import os
import sqlite3

class MsgDB:

    FOLDER_PATH = "Database"
    DATABASE_NAME = "DB.db"

    TABLE_NAME = "Messages"
    C_ID = "message_id"
    C_AUTHOR = "author"
    C_CONTENT = "content"
    C_CHANNEL = "channel"
    C_CATEGORY = "category"
    C_TIMESTAMP = "timestamp"
    C_MESSAGE_TYPE = "message_type"
    C_PARENT_MESSAGE_ID = "parent_message_id"
    C_KEYWORDS = "keywords"
    C_SENTIMENT_SCORE = "sentiment_score"

    CREATE_TABLE = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {C_ID} TEXT PRIMARY KEY,
        {C_AUTHOR} TEXT,
        {C_CONTENT} TEXT,
        {C_CHANNEL} TEXT,
        {C_CATEGORY} TEXT,
        {C_TIMESTAMP} TEXT,
        {C_MESSAGE_TYPE} TEXT,
        {C_PARENT_MESSAGE_ID} TEXT,
        {C_KEYWORDS} TEXT,
        {C_SENTIMENT_SCORE} REAL
    )
    """

    DB_PATH = os.path.join(FOLDER_PATH, DATABASE_NAME)

    # 初始化資料庫
    def __init__(self) -> None:

        # Creat Table
        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()  # 用 with 內的 conn 建立 cursor
            cursor.execute(self.CREATE_TABLE)
            conn.commit()

    # 連接資料庫
    def _connect_to_db(self) -> tuple:

        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row  # 讓結果以字典格式返回 ***

        return (conn, conn.cursor())
    
    def saveMessage(self, message_data: dict):
        
        conn, cursor = self._connect_to_db()

        query = f"""
        INSERT INTO {self.TABLE_NAME} (
            {self.C_ID}, {self.C_AUTHOR}, {self.C_CONTENT},
            {self.C_CHANNEL}, {self.C_CATEGORY}, {self.C_TIMESTAMP},
            {self.C_MESSAGE_TYPE}, {self.C_PARENT_MESSAGE_ID},
            {self.C_KEYWORDS}, {self.C_SENTIMENT_SCORE}
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            message_data.get(self.C_ID, None),
            message_data.get(self.C_AUTHOR, None),
            message_data.get(self.C_CONTENT, None),
            message_data.get(self.C_CHANNEL, None),
            message_data.get(self.C_CATEGORY, None),
            message_data.get(self.C_TIMESTAMP, None),
            message_data.get(self.C_MESSAGE_TYPE, None),
            message_data.get(self.C_PARENT_MESSAGE_ID, None),
            message_data.get(self.C_KEYWORDS, None),
            message_data.get(self.C_SENTIMENT_SCORE, None)
        ))

        conn.commit()
        conn.close()
    
    def getData(self, arg_text, arg_vars):
        
        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(arg_text, arg_vars)
            return cursor.fetchall()