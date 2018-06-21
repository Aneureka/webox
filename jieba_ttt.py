import jieba
import nltk
# nltk.download()

# print(list(jieba.cut('爱奇艺 - AI实习生')))
# print(list(jieba.cut('百度云计算 - 软件研发实习生')))
# print(list(jieba.cut('爱奇艺 - 广告算法实习生')))
# print(list(jieba.cut('爱奇艺 - AI实习生')))
# print(list(jieba.cut('【博瑞游戏】服务器程序实习生')))

sentence = '阿里巴巴爱我'
tokens = nltk.word_tokenize(sentence)
print(nltk.pos_tag(tokens))
print(tokens)