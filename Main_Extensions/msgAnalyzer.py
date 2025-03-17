import re
import discord
from ollama import generate
from discord.ext import commands, tasks
from Database.msgDB import MsgDB
from datetime import datetime, timedelta, time
import textwrap

import functools
import typing
import asyncio

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

class ChannelDropdown(discord.ui.Select):
    def __init__(self, channels, callback_function):

        self.callback_function = callback_function

        options = [
            discord.SelectOption(label=channel, value=channel) for channel in channels
        ]
        super().__init__(placeholder="選擇一個頻道", options=options)

    async def callback(self, interaction: discord.Interaction): await self.callback_function(self.values[0], interaction)

class ChannelSelectView(discord.ui.View):
    def __init__(self, channels, callback_function):
        super().__init__(timeout=60)  # 設定選單的存活時間
        self.add_item(ChannelDropdown(channels, callback_function))

class MsgAnalyzer(commands.Cog):

    allowed_categories = ["1335259735380983930"]
    send_channel_id = 1349594509738115072

    # Init : Bot and Database
    def __init__(self, bot) -> None:

        self.bot = bot
        self.message_database = MsgDB()

        if not self.send_scheduled_message.is_running():  # 確保定時任務不會重複啟動
            self.send_scheduled_message.start()

        send_channel_obj = bot.get_channel(self.send_channel_id)
        if send_channel_obj:
            self.send_channel = send_channel_obj.name  # 只存頻道名稱
        else:
            self.send_channel = None  # 避免 SQL 查詢時發生錯誤
    
    def _getChannels(self):
        """列出最近一週內有新訊息的頻道"""
        one_week_ago = datetime.now() - timedelta(days=7)

        placeholders = ",".join("?" * len(self.allowed_categories))

        # SQL 查詢參數
        query_params = [one_week_ago.isoformat(), *self.allowed_categories]

        # 構建 SQL 查詢
        sql_query = f"""
            SELECT DISTINCT {self.message_database.C_CHANNEL}
            FROM {self.message_database.TABLE_NAME}
            WHERE {self.message_database.C_TIMESTAMP} >= ?
            AND {self.message_database.C_CATEGORY} IN ({placeholders})
        """

        # 只有當 send_channel 存在時，才排除它
        if self.send_channel:
            sql_query += f" AND {self.message_database.C_CHANNEL} != ?"
            query_params.append(self.send_channel)

        result = self.message_database.getData(sql_query, query_params)

        return [row[0] for row in result]
    
    def _getChannelMessagesText(self, channel_name):
        """擷取特定頻道最近一週的所有訊息，並限制最大字數，包含時間戳和作者"""
        one_week_ago = datetime.now() - timedelta(days=7)

        result = self.message_database.getData(
            f"""
            SELECT {self.message_database.C_CONTENT}, {self.message_database.C_TIMESTAMP}, {self.message_database.C_AUTHOR} 
            FROM Messages 
            WHERE channel = ?
            AND timestamp >= ? 
            ORDER BY timestamp ASC;
            """,
            (channel_name, one_week_ago.isoformat())
        )

        # 格式化訊息，包括時間戳和作者
        messages = [
            f"[{row[1]}] {row[2]}: {row[0]}"
            for row in result
        ]

        # 轉換為單一文字
        return "\n".join(messages)
    
    @to_thread
    def _summarizeChannel(self, channel):
        """根據特定頻道生成摘要"""

        text = self._getChannelMessagesText(channel)

        # 使用 generate() 產生摘要
        response = generate(
            model='cwchang/llama3-taide-lx-8b-chat-alpha1:latest', 
            prompt=f"""
            請簡明扼要地總結以下聊天紀錄：
            
            {text}
            
            **要求：**
            1. 只包含對話的 **主要內容與結論**，忽略瑣碎細節與無關對話。
            2. 使用 **簡短、清晰的語言**，總結內容請控制在 **100 字以內**（如果對話內容較長，請用 3~5 句話概述）。
            3. 如果對話沒有重要內容，請回應「本頻道近期無重要對話」。
            """
        )

        # 確保獲取回應的內容
        summary = re.sub(
            r'<think>.*?</think>', '', 
            response["response"], flags=re.DOTALL
        ).strip()  # 這裡確保 summary 是字串

        return channel, summary
    
    async def callback_function(self, channel, interaction):
        await interaction.response.send_message(f"你選擇的頻道是：{channel}，請稍等 5~10 分鐘進行總結", ephemeral=True)
        start_time = datetime.now()
        channel, summary = await self._summarizeChannel(channel)
        elapsed_time = datetime.now() - start_time
        content = []
        content.append(f"對話頻道：{channel}")
        content.append(f"---")
        content.append(f"訊息摘要：\n{summary}")
        content.append(f"---")
        content.append(f"總結時間：{elapsed_time.total_seconds():.2f} 秒")
        text = textwrap.dedent("\n".join(content))
        await interaction.followup.send(content=text)

    @discord.app_commands.command(name="select_and_summarize_channel", description="選擇頻道並進行總結")
    async def select_and_summarize_channel(self, interaction: discord.Interaction):
        channels = self._getChannels()  # 取得頻道列表
        if not channels:
            await interaction.response.send_message("最近一週沒有活躍的頻道。", ephemeral=True)
            return

        # 假設你有一個 ChannelSelectView 類別
        view = ChannelSelectView(channels, self.callback_function)
        await interaction.response.send_message("請選擇你要總結的頻道：", view=view, ephemeral=True)

    @tasks.loop(weeks=5, time=time(hour=23, minute=0, second=0))  # 設定 UTC 23:01 → 台灣時間 07:01
    async def send_scheduled_message(self):
        print("start")
        send_channel = self.bot.get_channel(self.send_channel)
        if not send_channel: return

        start_time = datetime.now()

        channels = self._getChannels()
        print("資料庫中的頻道：", channels)

        results = await asyncio.gather(*(self._summarizeChannel(channel) for channel in channels))

        elapsed_time = datetime.now() - start_time

        # 輸出結果
        for channel, summary in results:
            content = []
            content.append(f"對話頻道：{channel}")
            content.append(f"---")
            content.append(f"訊息摘要：\n{summary}")
            content.append(f"---")
            await send_channel.send("\n".join(content))

        await send_channel.send(f"總結時間：{elapsed_time.total_seconds():.2f} 秒")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.send_scheduled_message.is_running():  # 確保不會重複啟動
            self.send_scheduled_message.start()

    @discord.app_commands.command(name="test_msg", description="測試訊息")
    async def test_msg(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"這是測試訊息。定時任務執行狀態: {self.send_scheduled_message.is_running()}")

async def setup(bot) : await bot.add_cog(MsgAnalyzer(bot))