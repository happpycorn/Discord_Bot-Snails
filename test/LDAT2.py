import os
import re
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib as plt
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker

import warnings
warnings.filterwarnings("ignore")

# Initialize drivers
print("Initializing drivers ... WS")
ws_driver = CkipWordSegmenter(model="bert-base", device=-1)
print("Initializing drivers ... POS")
pos_driver = CkipPosTagger(model="bert-base", device=-1)
print("Initializing drivers ... NER")
ner_driver = CkipNerChunker(model="bert-base", device=-1)
print("Initializing drivers ... all done")
print()

def read_stopword():

    with open(r"Asset\stopWords.txt", "r", encoding="utf-8") as f:
        stopwords = [word.strip("\n") for word in f.readlines()]
    return stopwords

stopwords = read_stopword()

def do_CKIP_WS(article):
    ws_results = ws_driver([str(article)])
    return ws_results