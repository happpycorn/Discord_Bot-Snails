import re
from ollama import generate
from msgDB import MsgDB
from datetime import datetime, timedelta

import functools
import typing
import asyncio

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

class MsgAnalyzer():
    FETCH_TIME_AREA = 8
    MODULE_NAME = 'cwchang/llama3-taide-lx-8b-chat-alpha1:latest'

    # Init : Bot and Database
    def __init__(self) -> None:

        self.message_database = MsgDB()
    
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

        summary = re.sub(
            r'<think>.*?</think>', '', 
            response["response"], flags=re.DOTALL
        ).strip()

        return channel, summary

    async def scheduled_message(self):

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

        response = generate(
            model=self.MODULE_NAME,
            prompt=f"""
            你是個專業的知識整理助手，請根據以下多個頻道的訊息摘要，撰寫一份高度濃縮、邏輯清楚的總結，方便各組成員快速了解整體狀況。
            請著重於：
            - 關鍵結論
            - 爭議或需要決策的事項
            - 下一步建議
            - 以組為單位撰寫摘要
            
            摘要資料如下：

            {text}
            """
        )

        return response