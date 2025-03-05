# Import
import os
import discord
from dotenv import load_dotenv
from discord import app_commands
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
    OWNER_ID = int(os.getenv("OWNER_ID"))
    EXT_LIST = [
        "Main_Extensions.msgSaver",
        "Main_Extensions.msgAnalyzer"
    ]

    # 初始化 Discord Bot
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=">", intents=intents)
    tree = bot.tree  # Slash 指令使用 `tree`

    bot.ws_driver = ws_driver
    bot.pos_driver = pos_driver

    def is_owner():
        async def predicate(interaction: discord.Interaction):
            return interaction.user.id == OWNER_ID
        return app_commands.check(predicate)

    @bot.event
    async def on_ready():
        for ext in EXT_LIST: await bot.load_extension(ext)
        await tree.sync()  # **同步 Slash 指令**
        print(f'Logged in as {bot.user}')

    # 載入擴充功能
    @tree.command(name="load_ext", description="載入或重新載入擴充功能（僅管理員可用）")
    @is_owner()
    async def load_ext(interaction: discord.Interaction, extension: str):
        """載入指定的擴充功能"""
        send = interaction.response.send_message
        try:
            if extension in bot.extensions:
                await bot.reload_extension(extension)
                action = "重新載入"
            else:
                await bot.load_extension(extension)
                action = "載入"

            await send(f"擴充功能 '{extension}' {action}開始！", ephemeral=True)
            await tree.sync()
            await send(f"擴充功能 '{extension}' {action}成功！", ephemeral=True)
        except Exception as e:
            await send(f"處理擴充功能 '{extension}' 時發生錯誤：{e}", ephemeral=True)

    @load_ext.error
    async def owner_only_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("🚫 你沒有權限使用這個指令！", ephemeral=True)

    # 卸載擴充功能
    @tree.command(name="unload_ext", description="卸載擴充功能（僅管理員可用）")
    @is_owner()
    async def unload_ext(interaction: discord.Interaction, extension: str):
        """卸載指定的擴充功能"""
        send = interaction.response.send_message
        try:
            await bot.unload_extension(extension)
            await send(f"擴充功能 '{extension}' 卸載成功！", ephemeral=True)
        except Exception as e:
            await send(f"卸載擴充功能 '{extension}' 時發生錯誤：{e}", ephemeral=True)

    @unload_ext.error
    async def owner_only_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("🚫 你沒有權限使用這個指令！", ephemeral=True)

    # 啟動 Bot
    bot.run(TOKEN)

if __name__ == "__main__":
    # 初始化模型
    initialize_models()

    # 啟動主程式
    main()