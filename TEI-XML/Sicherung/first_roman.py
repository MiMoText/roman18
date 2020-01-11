import re
import glob
import os.path


for document in glob.glob("D:/Downloads/roman-dixhuit/TEI-XML/Roman_bearbeitet/*.xml"):
    f = open(document, "r", encoding= 'utf8')
    clean = f.read()

    clean = '<text>'+clean+'</text>'
    clean = re.sub('<file name=".*?"/>', '', clean)
    clean = re.sub('<lb n=".*?"/>-+', '', clean)
    clean = re.sub ('<lb n=".*?"/><Z>-+</Z>', '', clean)
    clean = clean.replace('<i>', '<seg rend="italic">')
    clean = clean.replace('</i>', '</seg>')
    clean = clean.replace('<negEZ>', '')
    clean = clean.replace('</negEZ>', '')
    clean = clean.replace('<R>','')
    clean = clean.replace('</R>','')
    clean = re.sub('<pos up="\d">', '', clean)
    clean = clean.replace('</pos>','')
    clean = clean.replace('<Z>', '<head>')
    clean = clean.replace('</Z>', '</head>')
    clean = clean.replace('<h>', '<fw>')
    clean = clean.replace('</h>', '</fw>')
    clean = clean.replace('<footnotes/>', '<seg rend ="footnotes"/>')
    clean = clean.replace('<sup>', '')
    clean = clean.replace('</sup>', '')
    clean = clean.replace('<image/>', '<graphic/>')
    clean = clean.replace('<c>', '')
    clean = clean.replace('</c>', '')
    clean = clean.replace('n="E', 'n="''')
    clean = re.sub('<Ap\d>', '', clean)
    clean = re.sub('</Ap\d>', '', clean)
    clean = re.sub('<Am\d>', '<seg rend = "small">', clean)
    clean = re.sub('</Am\d>', '</seg>', clean)
    clean = re.sub('<INI\d>', '<seg rend = "caps"  type = "initials">', clean)
    clean = re.sub('</INI\d>', '</seg>', clean)
    clean = clean.replace('<P>','<p>')
    clean = clean.replace('</P>', '</p>')
    clean = clean.replace("^&", "&amp;")
    clean = re.sub('<lb n=".*?"/><konghang.*?>', '', clean)
    clean = clean.replace('<P/><p>', '')
    clean = clean.replace('</p><P/>', '')
    #'spr' destroys the XML-Order
    clean = clean.replace('<spr>', '')
    clean = clean.replace('</spr>', '')
    clean = re.sub('ſ', 's', clean)
    clean = re.sub('<fw><s n=".*?"/></fw>', '', clean)
    clean = re.sub('<s n=".*?"/>','', clean)
    clean = clean.replace('<E>','')
    clean = clean.replace('</E>', '')
    clean = clean.replace('〈zj-ym>','')
    clean = clean.replace('</zj-ym>','')
    clean = clean.replace('^%­{??}E', 'Ê')
    clean = clean.replace('<seg rend="italic"></seg>', '')
    clean = clean.replace('<hong>','')
    clean = clean.replace('</hong>','')
    clean = clean.replace('<seg rend="italic">;</seg>', ';')
    clean = clean.replace('<seg rend="italic">:</seg>', ':')
    clean = clean.replace('<seg rend="italic">!</seg>', '!')
    clean = clean.replace('<seg rend="italic">?</seg>', '?')
    clean = clean.replace('<tspb>', '')
    clean = clean.replace('</tspb>', '')



    #delete empy lines
    clean = [line for line in clean.split('\n') if line.strip() != '']


    #def adding(file):

   # lines = []
   # for line in file:
       # if line.startswith('<l>'):
        #    line += '</l>'
       # lines.append(line)
   # return lines


    #cleaned = adding(clean)
    cleaned = '\n'.join(clean)


    #print(cleaned)
    save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/xmls/'
    name = os.path.basename(document)
    fullname = os.path.join(save_path, name)
    fa = open(fullname, 'w', encoding="utf8")
    fa.write(cleaned)
    fa.close








