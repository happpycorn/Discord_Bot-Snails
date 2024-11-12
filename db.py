import sqlite3

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