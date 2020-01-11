import glob
import os.path
from bs4 import BeautifulSoup

for file in glob.glob('C:/Users/yulya/PycharmProjects/TEI-XML/xmls_for_plain/*.xml'):
    o = open(file, "r", encoding="utf8")
    inhalt = o.read()
    soup = BeautifulSoup(inhalt, "xml")
    plain = soup.body.get_text()
    plain = plain.replace('>','')
    #plain = [line for line in plain.split('\n') if line.strip() != '']
    #plain = '\n'.join(plain)
    plain = plain.replace('\n',' ')
    plain = plain.split('PARAGRAPH')
    plain = '\n'.join(plain)
    plain = plain.split('HEAD')
    plain = [line for line in plain if line.strip()!='']
    plain = '\n'.join(plain)

    save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/texts/'
    name = os.path.basename(file)
    name = name.replace('xml','txt')
    fullname = os.path.join(save_path, name)
    fa = open(fullname, 'w', encoding="utf8")
    fa.write(plain)
    fa.close
