from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

text = """
    在這寧靜的夜晚，滿天繁星閃耀，仿佛訴說著無數未解的秘密。微風輕拂，讓人感受到一絲絲的清涼與安寧。大地沉睡著，萬物都進入了休憩的時刻，唯有星光伴隨著夜行者，照亮他們前行的道路。
    是的，這樣的 SQL 語法是正確的。CREATE TABLE IF NOT EXISTS 可以在資料庫中創建一個名為 messages 的表格，並包含你指定的欄位。每個欄位的定義也很合理。以下是這段程式碼的結構說明：
    """

parser = PlaintextParser.from_string(text, Tokenizer("chinese"))
summarizer = LexRankSummarizer()
summary = summarizer(parser.document, 5)  # 設定摘要包含的句子數

for sentence in summary:
    print(sentence)
