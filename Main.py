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

    bot.ws_driver = ws_driver
    bot.pos_driver = pos_driver

    @bot.event
    async def on_ready() : print(f'Logged in as {bot.user}')

    @bot.command(name='load_extension')
    async def load_extension(ctx, extension : str):
        try : await bot.load_extension(extension) ; await ctx.send(f"Extension '{extension}' loaded successfully.")
        except Exception as e : await ctx.send(f"Failed to load extension '{extension}': {e}")

    @bot.command(name='unload_extension')
    async def unload_extension(ctx, extension : str):
        try : await bot.unload_extension(extension) ; await ctx.send(f"Extension '{extension}' unloaded successfully.")
        except Exception as e : await ctx.send(f"Failed to unload extension '{extension}': {e}")

    @bot.command(name='reload_extension')
    async def reload_extension(ctx, extension : str):
        try : await bot.reload_extension(extension) ; await ctx.send(f"Extension '{extension}' reloaded successfully.")
        except Exception as e : await ctx.send(f"Failed to reload extension '{extension}': {e}")

    # 啟動 Bot
    bot.run(TOKEN)

if __name__ == "__main__":
    # 初始化模型
    initialize_models()

    # 啟動主程式
    main()