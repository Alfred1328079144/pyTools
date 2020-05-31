#-*-conding:euc-kr-*-
from nltk import RegexpTokenizer

file = open("D:/workspace/zim/data/ko-wikibook.txt",encoding="utf-8")
tokenizer = RegexpTokenizer(".")
str.encode("utf-8")
lines = file.readlines()
for line in lines:
    sentences = tokenizer.tokenize(line)
    for sentences in sentences:
        print(sentences)

