
def read(file):
    file = open(file, 'r', encoding='utf8')
    stop = file.read()
    stop = stop.split()
    return stop


'''in this script we use our list with all words, where the hyphen was deleted from the step:"experiments_with_hyphen"
As we know that the most misspellings occur in connection with some prefixes and suffixes, we can make our
list shorter'''


def sort(list):
    sorted = []
    suffix=['moi','même','mêmes','tu', 'je','elle','il','ils','elles','vous']
    prefix=['très','bien','tout','toute','toutes']
    for word in list:
        for item in suffix:
            if word.endswith(item):
                sorted.append(word)
        for item in prefix:
            if word.startswith(item):
                sorted.append(word)
    return sorted


find = read('to_check.txt')
find = sort(find)
to_write=sorted(set(find))
with open('for_checking_final.txt','w', encoding='utf8') as text:
    text.write(str(to_write))