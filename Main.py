# Import
import json
import discord
from discord import app_commands
from discord.ext import commands
import traceback

def main():
    # Load config
    with open('config.json') as f: config = json.load(f)
    TOKEN = config['discord_token']
    ADMIN_ID = config['admin_id']

    EXT_LIST = [
        "Main_Extensions.msgSaver",
        "Main_Extensions.msgAnalyzer"
    ]

    # Init Discord Bot
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=None, intents=intents)
    tree = bot.tree

    # Permissions check decoration
    async def is_admin(interaction: discord.Interaction):
        return interaction.user.id == ADMIN_ID
    admin_only = app_commands.check(is_admin)

    # On ready function
    @bot.event
    async def on_ready():
        for ext in EXT_LIST:
            try:
                await bot.load_extension(ext)
                print(f"✅ Extension {ext} load success")
            except Exception as e: 
                print(f"❌ Load extension {ext} fail: {e}")
                print("Detailed error trace:")
                traceback.print_exc()
        await tree.sync()
        print(f'🤖 Logged in as {bot.user}')

    # Load extension function
    @tree.command(name="load_ext", description="↘️ Load or Reload extension (admin only)")
    @admin_only
    async def load_ext(interaction: discord.Interaction, extension: str):
        send = interaction.response.send_message
        try:
            if extension in bot.extensions:
                await bot.reload_extension(extension)
                action = "Reload"
            else:
                await bot.load_extension(extension)
                action = "Load"

            await tree.sync()
            await send(f"✅ {action} extension '{extension}' success!", ephemeral=True)
        except Exception as e:
            await send(f"❌ {action} extension '{extension}' failed. Error: {e}", ephemeral=True)

    # Unload extension function
    @tree.command(name="unload_ext", description="↖️ Unload extension (admin only)")
    @admin_only
    async def unload_ext(interaction: discord.Interaction, extension: str):
        send = interaction.response.send_message
        try:
            await bot.unload_extension(extension)
            await send(f"✅ Unload extension '{extension}' success!", ephemeral=True)
        except Exception as e:
            await send(f"❌ Proccess fail. Extension: '{extension}', fail: {e}", ephemeral=True)
    
    # List extension function
    @tree.command(name="list_ext", description="🔍 List extension (admin only)")
    @admin_only
    async def list_ext(interaction: discord.Interaction):
        extensions = list(bot.extensions.keys())
        send = interaction.response.send_message
        if extensions:
            extensions_list = "\n".join(extensions)
            await send(f"📋 Loaded extensions: \n{extensions_list}", ephemeral=True)
        else: await send("❌ Did not have any extension be load.", ephemeral=True)

    # Permission error proccess
    @load_ext.error
    @unload_ext.error
    @list_ext.error
    async def admin_only_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("❌ You do not have permission to use this command!", ephemeral=True)

    # Start Bot
    bot.run(TOKEN)

if __name__ == "__main__": main()