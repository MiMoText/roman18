import glob
import os.path
import csv
from bs4 import BeautifulSoup


path = 'C:/Users/yulya/PycharmProjects/TEI-XML/workxmls_formatted/*.xml'
metadata = 'roman18_ Übersicht.csv'
save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/header_test/'
if not os.path.exists(save_path):
    os.makedirs(save_path)


def filling_header(path, metadata):
    #read csv
    data = open(metadata,'r', encoding='utf8')
    mdata = csv.reader(data)
    for row in mdata:
        for file in glob.glob(path):
            #open and read file
            f = open(file, "r", encoding="utf8")
            r = f.read()
            r = r.replace('</hi> <hi rend = "italic">','')
            soup = BeautifulSoup(r, "xml")
            name = os.path.basename(file)
            id = name.replace('.xml','')
            if row[1] == id:
                #filling out author name, birth/death year and title
                a_name = row[4]+'('+row[2]+'-'+row[3]+')'
                title = row[6]+': MiMoText edition'
                tag = soup.author
                tag.string.replace_with(a_name)
                tag2 = soup.title
                tag2.string.replace_with(title)
                #filling out viaf id and wikidata id
                tag['ref'] = 'viaf:'+row[10]+';wikidata:'+row[9]
                #filling out author gender
                tag3 = soup.authorGender
                tag3['key'] = row[5][0].capitalize()
                #filling out first and print edition year
                tag4 = soup.ref
                tag4['target'] = row[8]
                tag5 = soup.find("bibl", type="firstEdition")
                tag6 = tag5.date
                tag6.string.replace_with(row[7])
                tag7 = soup.find("bibl", type="printSource")
                tag8 =tag7.date
                tag8.string.replace_with(row[7])
                fullname = os.path.join(save_path, name)
                fa = open(fullname, 'w', encoding="utf8")
                fa.write(str(soup))
                break
    return soup


def main():
    filling_header(path, metadata)


if __name__ == "__main__":
    main()