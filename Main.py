# Import
import json
import discord
from datetime import time, datetime
from discord.ext import tasks, commands

from msgSaver import MsgSaver
from msgAnalyzer import MsgAnalyzer

def main():
    # Load config
    with open('config.json') as f: config = json.load(f)
    TOKEN = config['discord_token']
    SEND_CHANNEL_ID = config['send_channel_id']

    # Init Discord Bot
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="/", intents=intents)
    tree = bot.tree

    # Define method
    msgSaver = MsgSaver()
    msgAnalyzer = MsgAnalyzer()

    # On ready function
    @bot.event
    async def on_ready():
        if not send_scheduled_message.is_running():
            send_scheduled_message.start()
        print(f'🤖 Logged in as {bot.user}')
    
    # On message function
    @bot.event
    async def on_message(message):
        if message.author.bot: return # 忽略機器人訊息
        msgSaver.saveMessage(message)

    @tasks.loop(time=time(hour=23, minute=0, second=0))  # 設定 UTC 23:01 → 台灣時間 07:01
    async def send_scheduled_message(self):
        if datetime.now().weekday() != 4: return
        channel = bot.get_channel(SEND_CHANNEL_ID)
        if not channel: return

        start_time = datetime.now()

        response = await msgAnalyzer.scheduled_message()
        await channel.send("\n".join(response))

        elapsed_time = datetime.now() - start_time
        await channel.send(f"總結時間：{elapsed_time.total_seconds():.2f} 秒")

    # Start Bot
    bot.run(TOKEN)

if __name__ == "__main__": main()