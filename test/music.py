from pytube import YouTube
import os
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = commands.Bot(command_prefix='%', intents=intents)
talk = set()


def endSong(path):

    # 刪除原文件

    os.remove(path)

    if len(playing_list) != 0:

        # 抓歌

        voice = discord.utils.get(client.voice_clients)
        url = playing_list[0]
        del playing_list[0]

        # 改名&播歌
        
        YouTube(url).streams.first().download()
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                os.rename(file,"song.mp4")
        
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"),after = lambda x: endSong("song.mp4"))

playing_list = []
async def play(ctx, url :str = ""):
    
    # 取得目前機器人狀態
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    # 如果機器人正在播放音樂, 將音樂放入播放清單
    if voice.is_playing():
        playing_list.append(url)
        print(playing_list)
        await ctx.send("把歌加到列表囉 *‘ v`*")
    
    # 如果機器人沒在播放, 開始準備要播放的音樂
    else:
    
        # 如果還有找到之前已經被播放過的音樂檔(沒播乾淨), 進行刪除
        song_there = os.path.isfile("song.mp4")
        
        try:
            if song_there:
                os.remove("song.mp4")
        except PermissionError:
            await ctx.send("發生了奇怪的事，請聯絡管理員 .w.")
        
        # 找尋輸入的Youtube連結, 將目標影片下載下來備用
        YouTube(url).streams.first().download()
        
        # 將目標影片改名, 方便找到它
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                os.rename(file,"song.mp4")
        # 找尋要播放的音樂並播放, 結束後依照after部分的程式進行後續步驟
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"),after = lambda x: endSong("song.mp4"))