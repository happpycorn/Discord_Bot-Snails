from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger

def load_stop_words(file_path):
    """
    從文件加載停用詞列表
    :param file_path: 停用詞文件路徑
    :return: 停用詞集合
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return set(word.strip() for word in f.readlines())

def process_text(text):
    """
    處理單條文本，返回分詞結果、詞性標註和關鍵詞
    """

    # 初始化分詞器與詞性標註器
    ws_driver = CkipWordSegmenter(model="bert-base")
    pos_driver = CkipPosTagger(model="bert-base")
    # 分詞
    word_splits = ws_driver([text])[0]

    # 詞性標註
    pos_tags = pos_driver([word_splits])[0]

    stop_words = load_stop_words(r"Asset\stopWords.txt")

    # 提取關鍵詞（名詞與動詞）
    keywords = [
        word for word, pos in zip(word_splits, pos_tags)
        if (pos.startswith("N") or pos.startswith("V")) and word not in stop_words
    ]

    return word_splits, pos_tags, keywords

def main():
    # 測試文本
    text = "樹莓派是一款非常受歡迎的小型計算機。"
    print(f"處理文本：{text}")

    # 處理文本
    word_splits, pos_tags, keywords = process_text(text)

    # 輸出結果
    print("分詞結果：", word_splits)
    print("詞性標註：", pos_tags)
    print("關鍵詞：", keywords)

if __name__ == '__main__': main()