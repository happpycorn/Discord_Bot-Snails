import json
from discord.ext import commands
from database.db import SqliteDataBase

class MessageCatcher(commands.Cog):

    # Read Config : Permitted Category and Channel
    with open('config.json', 'r') as f:
        config = json.load(f)

    permitted_category_ids = config.get("permitted_category_ids", [])
    permitted_channel_ids = config.get("permitted_channel_ids", [])

    # Init : Bot and Database
    def __init__(self, bot) -> None:

        self.bot = bot
        self.message_database = SqliteDataBase()
        self.message_database.createTable(
            '''
            CREATE TABLE IF NOT EXISTS messages
            (
                author TEXT,
                content TEXT,
                Keywords TEXT,
                message_id INTEGER PRIMARY KEY, 
                channel TEXT,
                category TEXT,
                timestamp TEXT
            )
            '''
        )

    # Catch Message
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user : return
        await self.bot.process_commands(message)

        if self.isSecretMessage(message) : return

        print(f"Received message: {message.content} from {message.author}")

        conn, cursor = self.message_database.connect_to_db()

        cursor.execute('INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)', 
        (
            str(message.author), 
            str(message.content), 
            self.getKeywords(str(message.content)),
            message.id, 
            str(message.channel), 
            str(message.channel.category.id), 
            str(message.created_at)
        ))

        conn.commit()
        conn.close()
    
    def isSecretMessage(self, message) -> bool:

        if message.channel.id in self.permitted_channel_ids : return True

        if message.channel.category.id in self.permitted_category_ids : return True

        return False
    
    def getKeywords(self, message : str) -> str:

        return "Nothing"