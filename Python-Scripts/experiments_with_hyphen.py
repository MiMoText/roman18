import re
import glob
import os.path


def read_file(file):
    f = open(file, 'r', encoding='utf8')
    roman = f.read()
    return roman


'''this is the last script for hyphen-cases: we take files from the previous step:"trennung_auflösen2" and 
stopwordlist from the step "bindestrich". First of all we check if a word with hyphen is in stopwordlist or not. 
If not, we delete hyphen. As hyphen may occur on the other place in word, we take a stopwordlist without 
hyphens and check whether our word is there. If we found our word, we add a hyphen with a help of a list 
with suffixes and prefixes'''


def deleting(file,stop):
    pl = []
    pl2 = []
    for x in re.findall(r'\w+(?:-\w+)+', file):
        if x not in stop:
            pl.append(x)
            y = x.replace('-','')
            pl2.append(y)
    return pl,pl2


def checking_without_hyphen(list1,list2):
    suffix = ['moi', 'même', 'mêmes', 'tu', 'je', 'elle', 'il', 'ils', 'elles', 'vous']
    prefix = ['très', 'bien', 'tout', 'toute', 'toutes']
    list = []
    list_final = []
    for item in list1:
        if item in list2:
            for x in suffix:
                if item.endswith(x) and item!='Estelle':
                    list.append(item)
                    word = item.replace(x,'-'+x)
                    list_final.append(word)
            for x in prefix:
                if item.startswith(x):
                    list.append(item)
                    word = item.replace(x, x+'-')
                    list_final.append(word)

    return list, list_final


def replacement(old_data, new_data, file):
    for index, replaced_word in enumerate(old_data):
        file = file.replace(replaced_word, new_data[index])
    return file


def main():
    stopwords = open('stopwords_full_version.txt', 'r', encoding='utf8')
    stop = stopwords.read()
    stop = stop.split()
    stopwords_without_hype = open('stopwords_full_version_without_hyphen.txt','r',encoding='utf8')
    stop2 = stopwords_without_hype.read()
    stop2 = stop2.split()
    new_stopwords=[]
    for document in glob.glob("C:/Users/yulya/PycharmProjects/TEI-XML/xmls_for_plain2/*.xml"):
        roman = read_file(document)
        changed = deleting(roman, stop)
        correct = replacement(changed[0], changed[1], roman)
        checking = checking_without_hyphen(changed[1],stop2)
        correct = replacement(checking[0],checking[1],correct)
        save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/xmls_for_plain3/'
        name = os.path.basename(document)
        fullname = os.path.join(save_path, name)
        fa = open(fullname, 'w', encoding="utf8")
        fa.write(correct)
        fa.close
        new_stopwords.extend(changed[1])


'''here we get the list of all words, where the hyphen was deleted. 
This list we used to add new stopwords'''

    #new_set = sorted(set(new_stopwords))
    #print(len(new_set))
    #with open('to_check.txt', 'w', encoding="utf8")as smth:
        #for word in new_set:
           # smth.write(word+' ')


if __name__ == "__main__":
    main()