from snownlp import SnowNLP

def calculate_sentiment_score(text):
    """
    使用 Snownlp 計算情緒分數
    :param text: 輸入文本
    :return: 情緒分數（範圍 0 到 1）
    """
    s = SnowNLP(text)
    return s.sentiments

def main():
    # 測試文本
    text = "客服態度冷漠，讓人非常不舒服。"
    print(f"處理文本：{text}")

    # 計算情緒分數
    sentiment_score = calculate_sentiment_score(text)
    print(f"情緒分數：{sentiment_score}")

if __name__ == '__main__':
    main()
