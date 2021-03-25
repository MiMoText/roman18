import glob
import os.path
import re


'''delete some elements to get well-formed-arbeitsxmls'''

for file in glob.glob('C:/Users/yulya/PycharmProjects/TEI-XML/xmls/*.xml'):
    f = open(file, "r", encoding="utf8")
    r = f.read()
    r = re.sub('<lb n=".*?"/>', '', r)
    r = [line for line in r.split('\n') if line.strip() != '']
    r = [line for line in r if not line.startswith('<fw>')]
    r = [line for line in r if not line.startswith('<graphic')]
    r = '\n'.join(r)
    save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/arbeitsxmls/'
    name = os.path.basename(file)
    fullname = os.path.join(save_path, name)
    fa = open(fullname, 'w', encoding="utf8")
    fa.write(r)





