import os
import sqlite3

class MsgDB:

    # Database setting
    FOLDER_PATH = "Database"
    DATABASE_NAME = "DB.db"
    DB_PATH = os.path.join(FOLDER_PATH, DATABASE_NAME)

    TABLE_NAME = "Messages"
    C_ID = "message_id"
    C_AUTHOR = "author"
    C_CONTENT = "content"
    C_CHANNEL = "channel"
    C_CATEGORY = "category"
    C_TIMESTAMP = "timestamp"

    # Database create command
    CREATE_TABLE = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {C_ID} TEXT PRIMARY KEY,
        {C_AUTHOR} TEXT,
        {C_CONTENT} TEXT,
        {C_CHANNEL} TEXT,
        {C_CATEGORY} TEXT,
        {C_TIMESTAMP} TEXT
    )
    """

    # Init database
    def __init__(self) -> None:

        # Creat Table
        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(self.CREATE_TABLE)
            conn.commit()

    # Connect to database
    def _connect_to_db(self) -> tuple:

        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row  # 讓結果以字典格式返回 ***

        return (conn, conn.cursor())
    
    # Save message
    def saveMessage(self, message_data: dict):
        
        conn, cursor = self._connect_to_db()

        query = f"""
        INSERT INTO {self.TABLE_NAME} (
            {self.C_ID}, {self.C_AUTHOR}, {self.C_CONTENT},
            {self.C_CHANNEL}, {self.C_CATEGORY}, {self.C_TIMESTAMP}
        ) VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            message_data.get(self.C_ID, None),
            message_data.get(self.C_AUTHOR, None),
            message_data.get(self.C_CONTENT, None),
            message_data.get(self.C_CHANNEL, None),
            message_data.get(self.C_CATEGORY, None),
            message_data.get(self.C_TIMESTAMP, None),
        ))

        conn.commit()
        conn.close()
    
    # Get data
    def getData(self, arg_text, arg_vars=()):
        
        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(arg_text, arg_vars)
            return cursor.fetchall()
    
    async def message_exists(self, message_id: int) -> bool:
        """檢查訊息是否已經在資料庫中"""
        query = f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE {self.C_ID} = {message_id}"
        result = self.getData(query)
        return result[0][0] > 0