import os
import discord
from discord.ext import commands
from pytube import YouTube
import Token
# from AI_return import AI_return
from Keyword import GREETING_COMMAND,FAREWELL_COMMAND,RETURN_WORD

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = commands.Bot(command_prefix='%', intents=intents)
talk = set()
playing_list = []
loop = True

# 當歌沒了
def endSong(path):
    # 刪除原文件
    os.remove(path)

    if playing_list:
        
        voice = discord.utils.get(client.voice_clients) # 取得機器人的音訊客戶端
        
        url = playing_list.pop(0) if not loop else playing_list[0] # 取得下一首歌曲的 URL 並且視狀況刪除連結
        
        download_and_rename(url) # 下載並重命名歌曲
        
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"), after=lambda x: endSong("song.mp4")) # 播放歌曲，播放結束後執行 endSong

def download_and_rename(url):
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

# 回應
async def all_return(message):
    
    global talk

    if not (message.content == GREETING_COMMAND or message.channel in talk) or message.content.startswith('%'):
        return

    if message.content == GREETING_COMMAND:
        talk.add(message.channel)
        text = RETURN_WORD["Hi"]
    
    elif message.content == FAREWELL_COMMAND:
        talk.remove(message.channel)
        text = RETURN_WORD["Bye"]
    
    elif message.channel in talk:
        try:
            pass
            # text =  AI_return(message.content)
        except:
            text = RETURN_WORD["Wait"]
    
    await message.channel.send(text)

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
    
    if message.content == GREETING_COMMAND or (message.channel in talk and not message.content.startswith('%')):
        await all_return(message)
    elif message.content.startswith('%'):
        await client.process_commands(message)

    return

# 加入語音
@client.command()
async def join(ctx):
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
@client.command()
async def leave(ctx):
    await ctx.message.delete()
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send(RETURN_WORD["What"])
        return

    await voice_client.disconnect()
    await ctx.send(RETURN_WORD["Leave"])

# 指令列表
client.remove_command('help')
@client.command()
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="指令列表", description=RETURN_WORD["Order"])
    await ctx.send(embeds=[embed])

# 播音樂
@client.command()
async def play(ctx, url :str = ""):
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
        playing_list.append(url)
        print(playing_list)
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
        download_and_rename(url)
        # 找尋要播放的音樂並播放, 結束後依照after部分的程式進行後續步驟
        voice.play(discord.FFmpegPCMAudio(executable="C:\Program Files\FFMPEG\\bin\\ffmpeg.exe", source="song.mp4"),after = lambda x: endSong("song.mp4"))
        await ctx.send(f"播放：{YouTube(url).title}")

# 切換循環
@client.command()
async def loopchange(ctx,change :str = ""):
    await ctx.message.delete()
    global loop
    if change:
        loop = not loop
    await ctx.send(f"loop == {loop}")

client.run(Token.dctoken)