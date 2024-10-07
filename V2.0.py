import os
import openai
import discord
from discord.ext import commands
from pytube import YouTube
from Keyword import *
from Token import *

commandscode = "%"

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = commands.Bot(command_prefix=commandscode, intents=intents)

# 音樂
class MusicPlay():
    def __init__(self):
        self.loopsta = True
        self.playing_list = []
    
    async def endSong(self, path):
        # 刪除原文件
        os.remove(path)

        if self.playing_list:
            
            voice = discord.utils.get(client.voice_clients) # 取得機器人的音訊客戶端
            
            url = self.playing_list.pop(0) if not self.loopsta else self.playing_list[0] # 取得下一首歌曲的 URL 並且視狀況刪除連結
            
            await self.download_and_rename(url) # 下載並重命名歌曲
            
            voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"), after=lambda x: self.endSong("song.mp4")) # 播放歌曲，播放結束後執行 endSong
    
    async def download_and_rename(self, url):
        song_path = "song.mp4"

        # 如果之前的歌曲尚未播放完畢，刪除原始檔案
        if os.path.exists(song_path):
            os.remove(song_path)

        # 下載歌曲
        YouTube(url).streams.first().download()

        # 尋找下載後的歌曲檔案並重命名
        for file in os.listdir("./"):
            if file.endswith(".mp4") or file.endswith(".3gpp"):
                os.rename(file, song_path)
    
    async def play(self, ctx, url):
        await ctx.message.delete()
        
        # 取得目前機器人狀態
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        
        if voice is None or not voice.is_connected():
            # 如果尚未連接，則連接到指令作者的語音頻道
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                voice = await channel.connect()
            else:
                await ctx.send(RETURN_WORD["Can'tFind"])
                return

        # 如果機器人正在播放音樂, 將音樂放入播放清單
        if voice.is_playing():
            self.playing_list.append(url)
            await ctx.send(RETURN_WORD["AddSong"])
        
        # 如果機器人沒在播放, 開始準備要播放的音樂
        else:
        
            # 如果還有找到之前已經被播放過的音樂檔(沒播乾淨), 進行刪除
            song_there = os.path.isfile("song.mp4")
            
            try:
                if song_there:
                    os.remove("song.mp4")
            except PermissionError:
                await ctx.send(RETURN_WORD["SomeIssueToSong"])
            await self.download_and_rename(url)
            # 找尋要播放的音樂並播放, 結束後依照after部分的程式進行後續步驟
            voice.play(discord.FFmpegPCMAudio(executable=R"C:\Program Files\FFMPEG\bin\ffmpeg.exe", source="song.mp4"),after = lambda x: self.endSong("song.mp4"))
            await ctx.send(f"播放：{YouTube(url).title}")
    
    # 加入語音
    async def join(self, ctx):
        await ctx.message.delete()
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send(RETURN_WORD["Can'tFind"])
            return
        channel = ctx.author.voice.channel
        voice_client = ctx.guild.voice_client
        
        if voice_client:
            await voice_client.move_to(channel)
        else:
            await channel.connect()

        await ctx.send(f"{RETURN_WORD['Comming']} (頻道：{channel.name})")

    # 退出語音
    async def leave(self, ctx):
        await ctx.message.delete()
        voice_client = ctx.guild.voice_client
        if not voice_client:
            await ctx.send(RETURN_WORD["What"])
            return

        await voice_client.disconnect()
        await ctx.send(RETURN_WORD["Leave"])

    # 迴圈控制
    async def loop(self, ctx, change):

        await ctx.message.delete()

        if change:
            self.loopsta = not self.loopsta

        await ctx.send(f"loop == {self.loopsta}")

# 回應
class ReturnBack:
    def __init__(self):
        self.talk = set()
        self.model = "gpt-3.5-turbo-instruct"
        openai.api_key = OPENAITOKEN

    async def help(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="指令列表", description=RETURN_WORD["Order"])
        await ctx.send(embeds=[embed])

    # 回應篩選
    async def all_return(self, message):

        if message.content == GREETING_COMMAND:
            self.talk.add(message.channel)
            text = RETURN_WORD["Hi"]
        
        elif message.content == FAREWELL_COMMAND:
            self.talk.remove(message.channel)
            text = RETURN_WORD["Bye"]
        
        else:
            try:
                text =  self.AI_return(message.content)
            except:
                text = RETURN_WORD["Wait"]
        
        await message.channel.send(text)
    
    def AI_return(self, my_input):
        response = openai.Completion.create(
            model=self.model,
            prompt=my_input+"，用繁體中文回答。",
            max_tokens=128,
            temperature=0.5,
        )

        completed_text = response["choices"][0]["text"]
        return completed_text

    async def confuse(self, message):
        await message.delete()
        embed = discord.Embed(description=message.content)
        await message.channel.send(embeds=[embed])

talker = ReturnBack()
musicplayer = MusicPlay()

# 初始化
@client.event
async def on_ready():
    print('目前登入身份：', client.user)
    state = discord.Activity(type=discord.ActivityType.watching, name="頂樓的望遠鏡")
    await client.change_presence(status=discord.Status.online, activity=state)
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible

# 偵測並回應
@client.event
async def on_message(message):
    if message.author == client.user: #防止迴圈
        return
    
    if message.content.startswith('%'):
        await client .process_commands(message)
    elif "小蝸的告解室" == str(message.channel):
        await talker.confuse(message)
    elif message.content == GREETING_COMMAND or message.channel in talker.talk:
        await talker.all_return(message)

# 指令列表
client.remove_command('help')
@client.command()
async def help(ctx):
    await talker.help(ctx)

# 播音樂
@client.command()
async def play(ctx, url :str = ""):
    await musicplayer.play(ctx, url)

# 迴圈
@client.command()
async def loop(ctx, change :int = ""):
    await musicplayer.loop(ctx, change)

@client.command()
async def join(ctx):
    await musicplayer.join(ctx)

@client.command()
async def leave(ctx):
    await musicplayer.leave(ctx)

client.run(DCTOKEN)