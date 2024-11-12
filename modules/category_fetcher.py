# 抓取類別的程式
async def list_categories(ctx):
    # 確保指令在伺服器中執行
    if not ctx.guild:
        await ctx.send("此指令只能在伺服器中使用！")
        return

    # 抓取所有類別
    categories = ctx.guild.categories
    if not categories:
        await ctx.send("此伺服器沒有任何類別。")
        return

    # 構建訊息內容
    category_list = "\n".join([f"類別名稱: {category.name} | 類別ID: {category.id}" for category in categories])
    
    # 發送類別列表
    print(category_list)