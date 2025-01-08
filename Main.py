# Import
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

# Load TOKEN
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)

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

bot.run(TOKEN)