import json
from discord.ext import commands
from Database.db import SqliteDataBase

class MsgSaver(commands.Cog):

    # Catch Message
    @commands.Cog.listener()
    async def on_message(self, message) -> None:

        if message.author == self.bot.user : return
        # await self.bot.process_commands(message)
        
        # Check if Message is from an Allowed Channel or Category
        # if self.isAllowMessage(message.channel) : self.SaveMessage(message)
        self.SaveMessage(message) # <- Or Just Use it

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

        # Read Config : Permitted Category and Channel
        with open(r'Asset\config.json', 'r') as f : config = json.load(f)

        self.allow_category_ids = config.get("allow_category_ids", [])
        self.allow_channel_ids = config.get("allow_channel_ids", [])
    
    # SaveMessage
    def SaveMessage(self, message) -> None:

        print(f"Received message: {message.content} from {message.author}")

        conn, cursor = self.message_database.connect_to_db()

        # Extract relevant message data
        author = str(message.author)
        content = str(message.content)
        keywords = self.getKeywords(content)
        message_id = message.id
        channel = str(message.channel)
        category = str(message.channel.category.id if message.channel.category else None)
        timestamp = str(message.created_at)

        # Execute SQL
        cursor.execute(
            '''
            INSERT OR IGNORE INTO messages 
            (author, content, keywords, message_id, channel, category, timestamp) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (author, content, keywords, message_id, channel, category, timestamp)
        )

        # Commit changes
        conn.commit()
        conn.close()
    
    # Check if Message is from an Allowed Channel or Category
    def isAllowMessage(self, m) -> bool:

        if m.id in self.allow_channel_ids : return True
        if m.category is not None and m.category.id in self.allow_category_ids : return True
        return False
    
    # Use LDA
    def getKeywords(self, message : str) -> str:

        return "Nothing"

async def setup(bot) : await bot.add_cog(MsgSaver(bot))