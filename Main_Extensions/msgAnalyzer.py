import json
import discord
from ollama import generate
from discord.ext import commands, tasks
from Database.msgDB import MsgDB
from datetime import datetime, timedelta, time, timezone

import functools
import typing
import asyncio

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

class MsgAnalyzer(commands.Cog):
    FETCH_TIME_AREA = 8
    MODULE_NAME = 'cwchang/llama3-taide-lx-8b-chat-alpha1:latest'

    # Init : Bot and Database
    def __init__(self, bot) -> None:

        self.bot = bot
        self.message_database = MsgDB()

        # Ensure that scheduled tasks are not started repeatedly
        if not self.send_scheduled_message.is_running():
            self.send_scheduled_message.start()

        # Read Config : Channel for send weekly reports
        with open(r'config.json', 'r') as f : config = json.load(f)
        self.send_channel_id = config.get("send_channel_id") or []
    
    # Get channels updated within a week
    def _getChannels(self):
        one_week_ago = datetime.now() - timedelta(days=self.FETCH_TIME_AREA)
        query_params = [one_week_ago.strftime("%Y-%m-%d %H:%M:%S")]

        # Constructing SQL queries
        sql_query = f"""
            SELECT DISTINCT {self.message_database.C_CHANNEL}
            FROM {self.message_database.TABLE_NAME}
            WHERE {self.message_database.C_TIMESTAMP} >= ?
        """

        # Exclude send channel if it exists
        if self.send_channel_id:
            sql_query += f" AND {self.message_database.C_CHANNEL} != ?"
            query_params.append(self.send_channel_id)

        result = self.message_database.getData(sql_query, query_params)
        return [] if not result else [row[0] for row in result]
    
    # Get channel updates for the week
    def _getChannelMessagesText(self, channel_name):
        one_week_ago = datetime.now() - timedelta(days=self.FETCH_TIME_AREA)

        result = self.message_database.getData(
            f"""
            SELECT {self.message_database.C_CONTENT}, {self.message_database.C_TIMESTAMP}, {self.message_database.C_AUTHOR} 
            FROM Messages 
            WHERE channel = ?
            AND timestamp >= ? 
            ORDER BY timestamp ASC;
            """,
            (channel_name, one_week_ago.strftime("%Y-%m-%d %H:%M:%S"))
        )

        messages = [
            f"[{datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%m/%d %H:%M')}] {row[2]}: {row[0]}"
            for row in result
        ]

        # Convert to String
        return "\n".join(messages)
    
    # Generate a summary based on a specific channel
    @to_thread
    def _summarizeChannel(self, channel):
        text = self._getChannelMessagesText(channel)

        response = generate(
            model=self.MODULE_NAME,
            prompt=f"""
            請簡明扼要地總結以下聊天紀錄：
            
            {text}
            
            **要求：**
            1. 只包含對話的 **主要內容與結論**，忽略瑣碎細節與無關對話。
            2. 使用 **簡短、清晰的語言**，總結內容請控制在 **100 字以內**（如果對話內容較長，請用 3~5 句話概述）。
            3. 如果對話沒有重要內容，請回應「本頻道近期無重要對話」。
            """
        )

        return channel, response["response"]
    
    @to_thread
    def _summarizeSummarize(self, summarize):
        response = generate(
            model=self.MODULE_NAME,
            prompt=f"""
            你是個專業的知識整理助手，請根據以下多個頻道的訊息摘要，撰寫一份高度濃縮、邏輯清楚的總結，方便各組成員快速了解整體狀況。
            請著重於：
            - 關鍵結論
            - 爭議或需要決策的事項
            - 下一步建議
            - 以組為單位撰寫摘要

            這之中主要可以分為三組，分別是航電組、結構組與酬載組，麻煩將訊息分為這三組，並依照上面的規則進行整理
            
            摘要資料如下：

            {summarize}
            """
        )
        return response["response"]

    
    @tasks.loop(time=time(hour=2, minute=50, second=0))  # 設定 UTC 23:01 → 台灣時間 07:01
    async def send_scheduled_message(self):

        if datetime.now(timezone.utc).weekday() != 1: return # 星期五是 `4`，不是的話就跳過
        
        print("start")
        send_channel = self.bot.get_channel(self.send_channel_id)
        if not send_channel: return

        start_time = datetime.now()

        channels = self._getChannels()
        print("資料庫中的頻道：", channels)

        results = await asyncio.gather(*(self._summarizeChannel(channel) for channel in channels))

        print("第一階段完成")

        # 輸出結果
        content = []
        for channel, summary in results:
            content.append(f"對話頻道：{channel}")
            content.append(f"---")
            content.append(f"訊息摘要：\n{summary}")
            content.append(f"---")
        text = "\n".join(content)

        response = await self._summarizeSummarize(text)

        print(response)
        await send_channel.send(response)

        elapsed_time = datetime.now() - start_time
        await send_channel.send(f"總結時間：{elapsed_time.total_seconds():.2f} 秒")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.send_scheduled_message.is_running():  # 確保不會重複啟動
            self.send_scheduled_message.start()

    @discord.app_commands.command(name="test_msg", description="測試訊息")
    async def test_msg(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"這是測試訊息。定時任務執行狀態: {self.send_scheduled_message.is_running()}")

async def setup(bot) : await bot.add_cog(MsgAnalyzer(bot))