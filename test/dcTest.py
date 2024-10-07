import discord
from Token import DCTOKEN

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
talk = []

@client.event
async def on_ready():
    print('目前登入身份：', client.user)
    state = discord.Activity(type=discord.ActivityType.watching, name="頂樓的望遠鏡")
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await client.change_presence(status=discord.Status.online, activity=state)

@client.event
async def on_message(message):
    global talk
    if message.author == client.user:
        return
    
    if message.content == "Hi小蝸":
        await message.channel.send("Hi你好:D")
        talk.append(message.channel)
        return
    elif message.content == "拜拜小蝸":
        await message.channel.send("拜拜，祝你有美好的一天>w<")
        while message.channel in talk:
            talk.remove(message.channel)
        return
    elif message.channel in talk:
        await message.channel.send(message.content)
        return

client.run(DCTOKEN)