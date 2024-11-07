import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from db import MessageManager, MessageAnlyzer

# 載入 TOKEN
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 設定機器人
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 引入程式
messageManager = MessageManager()
messageAnlyzer = MessageAnlyzer()

# 當機器人準備完成
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# 指令：抓取指定頻道中近一週的訊息
@bot.command()
async def fetch_recent_messages(ctx):
    await messageManager.fetch_recent_messages(ctx)

@bot.command()
async def data_send(ctx, data_type: str):
    await messageAnlyzer.data_send(ctx, data_type)

bot.run(TOKEN)