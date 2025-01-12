import os
import sqlite3

class MsgDB:

    FOLDER_PATH = "Database"
    DATABASE_NAME = "DB.db"

    TABLE_NAME = "Messages"
    COLUMN_ID = "message_id"
    COLUMN_AUTHOR = "author"
    COLUMN_CONTENT = "content"
    COLUMN_CHANNEL = "channel"
    COLUMN_CATEGORY = "category"
    COLUMN_TIMESTAMP = "timestamp"
    COLUMN_MESSAGE_TYPE = "message_type"
    COLUMN_PARENT_MESSAGE_ID = "parent_message_id"
    COLUMN_KEYWORDS = "keywords"
    COLUMN_SENTIMENT_SCORE = "sentiment_score"

    CREATE_TABLE = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {COLUMN_ID} TEXT PRIMARY KEY,
        {COLUMN_AUTHOR} TEXT,
        {COLUMN_CONTENT} TEXT,
        {COLUMN_CHANNEL} TEXT,
        {COLUMN_CATEGORY} TEXT,
        {COLUMN_TIMESTAMP} TEXT,
        {COLUMN_MESSAGE_TYPE} TEXT,
        {COLUMN_PARENT_MESSAGE_ID} TEXT,
        {COLUMN_KEYWORDS} TEXT,
        {COLUMN_SENTIMENT_SCORE} REAL
    )
    """

    DB_PATH = os.path.join(FOLDER_PATH, DATABASE_NAME)

    # 初始化資料庫
    def __init__(self) -> None:

        # Creat Table
        conn, cursor = self.connect_to_db()
        cursor.execute(self.CREATE_TABLE)
        conn.commit()
        conn.close()

    # 連接資料庫
    def connect_to_db(self) -> tuple:

        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row  # 讓結果以字典格式返回 ***

        return (conn, conn.cursor())
    
    def saveMessage(self, message_data: dict):
        
        conn, cursor = self.connect_to_db()

        query = f"""
        INSERT INTO {self.TABLE_NAME} (
            {self.COLUMN_ID}, {self.COLUMN_AUTHOR}, {self.COLUMN_CONTENT},
            {self.COLUMN_CHANNEL}, {self.COLUMN_CATEGORY}, {self.COLUMN_TIMESTAMP},
            {self.COLUMN_MESSAGE_TYPE}, {self.COLUMN_PARENT_MESSAGE_ID},
            {self.COLUMN_KEYWORDS}, {self.COLUMN_SENTIMENT_SCORE}
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            message_data.get(self.COLUMN_ID, None),
            message_data.get(self.COLUMN_AUTHOR, None),
            message_data.get(self.COLUMN_CONTENT, None),
            message_data.get(self.COLUMN_CHANNEL, None),
            message_data.get(self.COLUMN_CATEGORY, None),
            message_data.get(self.COLUMN_TIMESTAMP, None),
            message_data.get(self.COLUMN_MESSAGE_TYPE, None),
            message_data.get(self.COLUMN_PARENT_MESSAGE_ID, None),
            message_data.get(self.COLUMN_KEYWORDS, None),
            message_data.get(self.COLUMN_SENTIMENT_SCORE, None)
        ))

        conn.commit()
        conn.close()