from discord.ext import commands

class CommandExtension(commands.Cog):

    def __init__(self, bot) : self.bot = bot

    # Get categories
    @commands.command()
    async def list_categories(self, ctx):

        # Ensure the command is executed in a server
        if not ctx.guild:
            await ctx.send("This command can only be used in a server!")
            return

        # Fetch all categories
        categories = ctx.guild.categories

        if not categories:
            await ctx.send("This server has no categories.")
            return

        # Build the message content
        category_list = "\n".join([f"Category Name: {category.name} | Category ID: {category.id}" for category in categories])
        
        # Send category list
        print(category_list)
        await ctx.send("The data has been sent to the backend.")

def setup(bot):
    bot.add_cog(CommandExtension(bot))