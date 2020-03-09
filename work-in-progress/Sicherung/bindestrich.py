import re
import glob


def generate_stopwords(path):
    stopwords = []
    for file in glob.glob(path):
        f = open(file, "r", encoding="utf8")
        r = f.read()
        words = re.findall(r'\w+(?:-\w+)+', r)
        stopwords.extend(words)
    return stopwords


path ='C:/Users/yulya/PycharmProjects/TEI-XML/xmls_for_plain/*.xml'
result = generate_stopwords(path)
result = set(result)

with open('stopwords.txt', "w", encoding = 'utf8') as file:
    for word in result:
        file.write(word+' ')
