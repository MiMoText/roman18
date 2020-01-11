import re

with open('Popeliniere_Daira_test.txt', "r", encoding="utf8")as text:
    roman = text.read()

roman = roman.replace('- ','-')
stopwords = open('stopwords.txt', 'r',encoding= 'utf8')
stop = stopwords.read()
stop = stop.split()


def deleting(file):
    pl = []
    pl2 = []
    for x in re.findall(r'\w+(?:-\w+)+', file):
        if x not in stop:
            pl.append(x)
            y = x.replace('-','')
            pl2.append(y)

    return pl,pl2


def replacement(old_data, new_data, file):
    for index, replaced_word in enumerate(old_data):
        file = file.replace(replaced_word, new_data[index])
    return file




roma  = deleting(roman)
list1 = roma[0]
list2 = roma[1]
final = replacement(list1,list2,roman)
final = final.replace(' -',' - ')
print(final)
with open('Popeliniere_Daira_test2.txt', "w", encoding="utf8") as text:
    text.write(final)