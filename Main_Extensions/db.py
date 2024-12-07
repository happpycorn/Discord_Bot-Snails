import os
import sqlite3

class SqliteDataBase:

    # 初始化資料庫
    def __init__(self, db_path : str = "Message") -> None:
        
        folder_path = "Database"
        self.db_path = os.path.join(folder_path, db_path)

    # 連接資料庫
    def connect_to_db(self) -> tuple:

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 讓結果以字典格式返回 ***

        return (conn, conn.cursor())

    def createTable(self, rule : str):

        conn, cursor = self.connect_to_db()
        cursor.execute(rule)
        conn.commit()
        conn.close()