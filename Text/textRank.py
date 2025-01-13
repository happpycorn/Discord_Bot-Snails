from snownlp import SnowNLP

def summarize_with_snownlp(messages, num_sentences=3):
    """
    使用 SnowNLP 對一段文本生成摘要。
    Args:
        messages (list): 文本列表，每條消息是一個字符串。
        num_sentences (int): 提取的摘要句數。

    Returns:
        list: 摘要句子列表。
    """
    # 合併所有消息為一段文本
    text = chr(65292).join(messages)
    
    # 生成摘要
    s = SnowNLP(text)
    summary = s.summary(num_sentences)
    return summary

messages = [
    "我遇到了問題",
    "問題似乎解決了",
    "請問這個系統該如何安裝？",
    "樹莓派是一款非常受歡迎的小型計算機。"
]

summary = summarize_with_snownlp(messages, num_sentences=2)
print("摘要結果：", summary)