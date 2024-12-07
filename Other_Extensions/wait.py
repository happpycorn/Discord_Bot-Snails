  
# 傳送資料
@bot.command()
async def popular_channel(ctx):
    await messageAnlyzer.popular_channel(ctx)

# 文字雲
@bot.command()
async def draw_word_cloud(ctx):
    await messageAnlyzer.draw_word_cloud(ctx)

# 抓取類別
@bot.command()
async def list_categories(ctx):
    await list_categories(ctx)