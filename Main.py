# Import
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger

# 定義模型
ws_driver = None
pos_driver = None

def initialize_models():
    global ws_driver, pos_driver
    ws_driver = CkipWordSegmenter(model="bert-base")
    pos_driver = CkipPosTagger(model="bert-base")
    print("Models initialized successfully.")

def main():
    # Load TOKEN
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    # 初始化 Discord Bot
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=">", intents=intents)
    tree = bot.tree  # Slash 指令使用 `tree`

    bot.ws_driver = ws_driver
    bot.pos_driver = pos_driver

    @bot.event
    async def on_ready():
        await tree.sync()  # **同步 Slash 指令**
        print(f'Logged in as {bot.user}')

    # 傳統指令：載入擴充功能
    @bot.command(name="load_ext", help="載入或重新載入擴充功能")
    async def load_ext(ctx, extension: str):
        try:
            if extension in bot.extensions:
                await bot.reload_extension(extension)
                action = "重新載入"
            else:
                await bot.load_extension(extension)
                action = "載入"

            await ctx.send(f"擴充功能 '{extension}' {action}開始！")
            await tree.sync()
            await ctx.send(f"擴充功能 '{extension}' {action}成功！")
        except Exception as e:
            await ctx.send(f"處理擴充功能 '{extension}' 時發生錯誤：{e}")

    # 傳統指令：卸載擴充功能
    @bot.command(name="unload_ext", help="卸載擴充功能")
    async def unload_ext(ctx, extension: str):
        """卸載指定的擴充功能"""
        try:
            await bot.unload_extension(extension)
            await ctx.send(f"擴充功能 '{extension}' 卸載成功！")
        except Exception as e:
            await ctx.send(f"卸載擴充功能 '{extension}' 時發生錯誤：{e}")

    # 啟動 Bot
    bot.run(TOKEN)

if __name__ == "__main__":
    # 初始化模型
    initialize_models()

    # 啟動主程式
    main()