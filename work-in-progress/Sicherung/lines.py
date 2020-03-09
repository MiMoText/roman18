import glob
import os.path

for file in glob.glob('C:/Users/yulya/PycharmProjects/TEI-XML/xmls/*.xml'):
    f = open(file, "r", encoding="utf8")
    r = f.read()
    r = r.replace('</p>', 'PARAGRAPH </p>')
    r = r.replace('</head>', 'HEAD </head>')
    save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/xmls_for_plain/'
    name = os.path.basename(file)
    fullname = os.path.join(save_path, name)
    fa = open(fullname, 'w', encoding="utf8")
    for line in r:
        if '<fw>' not in line:
            fa.write(line)




