import jieba
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

np.set_printoptions(precision=2) # 設小數點兩位(顯示設定)

# 定義分詞函數
def chinese_tokenizer(text):
    return jieba.lcut(text)

# 準備中文文本
docs = np.array([
    '在這寧靜的夜晚，滿天繁星閃耀，仿佛訴說著無數未解的秘密。微風輕拂，讓人感受到一絲絲的清涼與安寧。大地沉睡著，萬物都進入了休憩的時刻，唯有星光伴隨著夜行者，照亮他們前行的道路。'
])

# 使用自定義分詞器
tfidf = TfidfTransformer(use_idf=True, norm = 'l2', smooth_idf=True)
count = CountVectorizer(tokenizer=chinese_tokenizer)

bag = tfidf.fit_transform(count.fit_transform(docs)).toarray()

# 計算出現多少個單字，並幫他們做編號
print(count.vocabulary_)

# 依照上面印出來的編號，再去對照在文句中出現的次數
print(bag)