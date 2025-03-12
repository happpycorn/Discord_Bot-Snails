import discord
from datetime import time
from discord.ext import commands, tasks

class Noter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot  # 初始化 bot
        if not self.send_scheduled_message.is_running():  # 確保定時任務不會重複啟動
            self.send_scheduled_message.start()

    @tasks.loop(time=time(hour=0, minute=52, second=0))  # 設定 UTC 23:01 → 台灣時間 07:01
    async def send_scheduled_message(self):
        channel = self.bot.get_channel(1286549443071447112)
        if channel:
            await channel.send("早安！這是每天早上 7 點的自動訊息 🌅")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.send_scheduled_message.is_running():  # 確保不會重複啟動
            self.send_scheduled_message.start()

    @discord.app_commands.command(name="test_msg", description="測試訊息")
    async def test_msg(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"這是測試訊息。定時任務執行狀態: {self.send_scheduled_message.is_running()}")

async def setup(bot): await bot.add_cog(Noter(bot))
