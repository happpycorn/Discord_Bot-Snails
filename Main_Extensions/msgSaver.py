import json
from typing import Callable
from snownlp import SnowNLP
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
    def __init__(self, bot, isAllowGetAllMsg=True, messageAllowRule: Callable[[any], bool] = None) -> None:

        if messageAllowRule is None: self._isAllowMessage: Callable[[any], bool] = self._defaultMessageAllowRule
        else: self._isAllowMessage: Callable[[any], bool] = messageAllowRule

        self.bot = bot
        self.isAllowGetAllMsg = isAllowGetAllMsg
        self.msgDB = MsgDB()

        # Read Config : Permitted Category and Channel
        with open(r'Asset\config.json', 'r') as f : config = json.load(f)

        self.allow_category_ids = config.get("allow_category_ids", [])
        self.allow_channel_ids = config.get("allow_channel_ids", [])

        # Read Stop Words
        with open(r'Asset\stopWords.txt', "r", encoding="utf-8") as f:
            stop_words = set(word.strip() for word in f.readlines())
        
        self.stop_words = stop_words

        # 模型初始化狀態
        self.ws_driver = bot.ws_driver
        self.pos_driver = bot.pos_driver

    # SaveMessage
    def _saveMessage(self, message) -> None:

        print(f"Received message: {message.content} from {message.author}")

        message_data = {
            self.msgDB.C_ID: str(message.id),
            self.msgDB.C_AUTHOR: str(message.author),
            self.msgDB.C_CONTENT: str(message.content),
            self.msgDB.C_CHANNEL: str(message.channel),
            self.msgDB.C_CATEGORY: str(getattr(message.channel.category, 'id', None)),
            self.msgDB.C_TIMESTAMP: message.created_at.isoformat(),
            self.msgDB.C_MESSAGE_TYPE: str(message.type),
            self.msgDB.C_PARENT_MESSAGE_ID: str(getattr(message.reference, 'message_id', None)),
            self.msgDB.C_KEYWORDS: self._getKeywords(message),
            self.msgDB.C_SENTIMENT_SCORE: self._getScore(message)
        }

        self.msgDB.saveMessage(message_data)
    
    # Check if Message is from an Allowed Channel or Category
    def _defaultMessageAllowRule(self, m) -> bool:

        is_in_channel = m.id in self.allow_channel_ids
        is_in_category = m.category and m.category.id in self.allow_category_ids

        return is_in_channel or is_in_category
    
    # Use LDA
    def _getKeywords(self, message) -> str:

        text = str(message.content)
        if len(text) == 0: return None

        word_splits = self.ws_driver([text])[0]
        pos_tags = self.pos_driver([word_splits])[0]

        keywords = [
            word for word, pos in zip(word_splits, pos_tags)
            if (pos.startswith("N") or pos.startswith("V")) and word not in self.stop_words
        ]

        return ",".join(keywords)
    
    def _getScore(self, message) -> float:

        text = str(message.content).strip()  # 確保為字符串並去掉多餘空格
        if len(text) == 0: return None

        if not text: return 0.5

        try:
            s = SnowNLP(text)
            return s.sentiments
        except Exception as e:
            print(f"Error calculating sentiment score: {e}")
            return 0.5  # 當出現例外時返回中性分數

async def setup(bot) : await bot.add_cog(MsgSaver(bot))