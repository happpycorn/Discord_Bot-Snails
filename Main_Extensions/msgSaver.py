import json
from discord.ext import commands
from Database.msgDB import MsgDB

class MsgSaver(commands.Cog):

    # Catch Message
    @commands.Cog.listener()
    async def on_message(self, message) -> None:

        if message.author == self.bot.user: return

        if self.isAllowGetAllMsg or self._isAllowMessage(message.channel):
            self._saveMessage(message)

    # Init : Bot and Database
    def __init__(self, bot) -> None:

        self.bot = bot
        self.msgDB = MsgDB()

        # Read Config : Permitted Category and Channel
        with open(r'config.json', 'r') as f : config = json.load(f)

        self.allow_category_ids = config.get("allow_category_ids") or []
        self.allow_channel_ids = config.get("allow_channel_ids") or []
        self.isAllowGetAllMsg = not (self.allow_category_ids or self.allow_channel_ids)

    # Save message
    def _saveMessage(self, message) -> None:

        print(f"Received message: {message.content} from {message.author}")

        message_data = {
            self.msgDB.C_ID: str(message.id),
            self.msgDB.C_AUTHOR: str(message.author),
            self.msgDB.C_CONTENT: str(message.content),
            self.msgDB.C_CHANNEL: str(message.channel.id),
            self.msgDB.C_CATEGORY: str(getattr(message.channel.category, 'id', None)),
            self.msgDB.C_TIMESTAMP: message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.msgDB.saveMessage(message_data)
    
    # Check if Message is from an Allowed Channel or Category
    def _isAllowMessage(self, m) -> bool:

        is_in_channel = m.id in self.allow_channel_ids
        is_in_category = m.category and m.category.id in self.allow_category_ids

        return is_in_channel or is_in_category

async def setup(bot) : await bot.add_cog(MsgSaver(bot))