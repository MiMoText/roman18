import re
import glob

''' this function reads an xml-file, finds all words with hyphen
 and adds they to the list'''


def generate_stopwords(path):
    stopwords = []
    for file in glob.glob(path):
        f = open(file, "r", encoding="utf8")
        r = f.read()
        words = re.findall(r'\w+(?:-\w+)+', r)
        stopwords.extend(words)
    return stopwords


path = 'C:/Users/yulya/PycharmProjects/TEI-XML/xmls/*.xml'
result = generate_stopwords(path)

# set deletes all duplicates, so we get a list with unique words
result = set(result)
print(len(result))

'''to save results we need to separate the words not with commas, but with spaces,
so we can match the words in the text'''

with open('stopwords.txt', "w", encoding = 'utf8') as file:
    for word in result:
        file.write(word+' ')
