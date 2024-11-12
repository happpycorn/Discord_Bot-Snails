import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from modules.message_saver import MessageCatcher
from modules.message_analyzer import MessageAnlyzer
from modules.category_fetcher import list_categories

# 載入 TOKEN
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 設定機器人
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 引入程式
messageManager = MessageCatcher()
messageAnlyzer = MessageAnlyzer()

# 當機器人準備完成
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    await messageManager.add_message(message)
    await bot.process_commands(message)
    
# 傳送資料
@bot.command()
async def popular_channel(ctx):
    await messageAnlyzer.popular_channel(ctx)

# 文字雲
@bot.command()
async def draw_word_cloud(ctx):
    await messageAnlyzer.draw_word_cloud(ctx)

# 抓取類別
@bot.command()
async def list_categories(ctx):
    await list_categories(ctx)

bot.run(TOKEN)