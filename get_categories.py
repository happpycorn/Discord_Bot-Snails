import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 初始化機器人
intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# 抓取所有類別的指令
@bot.command(name="list_categories")
async def list_categories(ctx):
    # 確保指令在伺服器中執行
    if not ctx.guild:
        await ctx.send("此指令只能在伺服器中使用！")
        return

    # 抓取所有類別
    categories = ctx.guild.categories
    if not categories:
        await ctx.send("此伺服器沒有任何類別。")
        return

    # 構建訊息內容
    category_list = "\n".join([f"類別名稱: {category.name} | 類別ID: {category.id}" for category in categories])
    
    # 發送類別列表
    print(category_list)

# 啟動機器人
bot.run(TOKEN)