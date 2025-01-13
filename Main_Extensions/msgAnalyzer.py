from discord.ext import commands
from Database.msgDB import MsgDB
from collections import Counter

class MsgAnalyzer(commands.Cog):

    # Init : Bot and Database
    def __init__(self, bot) -> None:

        self.bot = bot
        self.message_database = MsgDB()

        self._genReport()
    
    def _genReport(self):

        data = self.message_database.getMessage()

        top_keywords = self._topKeywordCount(data, num=10)
        channel_data = self._channelDataCount(data)

        print("Top Keywords:", top_keywords)
        print("Channel Summary:\n", channel_data)

    def _topKeywordCount(self, data, num : int = 10):

        keywords = data["keywords"].apply(lambda x: x.split(",") if isinstance(x, str) and x else [])
        all_keywords = Counter([word for keywords in keywords for word in keywords if len(word) > 1])
        top_keywords = all_keywords.most_common(num)

        return top_keywords

    def _channelDataCount(self, data):
        channel_data = data.groupby("channel").agg(
            message_count=("message_id", "count"),  # 消息數量
            average_sentiment=("sentiment_score", "mean")  # 平均情緒分數
        ).reset_index()
        return channel_data

async def setup(bot) : await bot.add_cog(MsgAnalyzer(bot))