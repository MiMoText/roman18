import re
import glob
import os.path

'''open document and read file'''

def changing(path):

    f = open(path, "r", encoding= 'utf8')
    clean = f.read()

    #insert root-tag to make xml well-formed
    clean = '<text>'+clean+'</text>'

    #delete and change some elements
    clean = re.sub('<file name=".*?"/>', '', clean)
    clean = re.sub('<lb n=".*?"/>-+', '', clean)
    clean = re.sub ('<lb n=".*?"/><Z>-+</Z>', '', clean)
    clean = clean.replace('<c><i>', '<hi rend="italic; small caps">')
    clean = clean.replace('</i></c>', '</hi>')
    clean = clean.replace('<i>', '<hi rend="italic">')
    clean = clean.replace('</i>', '</hi>')
    clean = clean.replace('<negEZ>', '<p>')
    clean = clean.replace('</negEZ>', '</p>')
    clean = clean.replace('<R>','')
    clean = clean.replace('</R>','')
    clean = re.sub('<pos up="\d">', '', clean)
    clean = clean.replace('</pos>','')
    clean = clean.replace('<Z><image/></Z>','<graphic/>')
    clean = clean.replace('<Z>', '<head>')
    clean = clean.replace('</Z>', '</head>')
    clean = clean.replace('<h>', '<fw>')
    clean = clean.replace('</h>', '</fw>')
    clean = clean.replace('<footnotes/>', '<note type="footnote">')
    clean = clean.replace('<sup>', '')
    clean = clean.replace('</sup>', '')
    clean = clean.replace('<image/>', '<graphic/>')
    clean = clean.replace('<c>', '<hi rend="small caps">')
    clean = clean.replace('</c>', '</hi>')
    clean = clean.replace('n="E', 'n="''')
    clean = re.sub('<Ap\d>', '', clean)
    clean = re.sub('</Ap\d>', '', clean)
    clean = re.sub('<Am\d>', '<hi rend="small">', clean)
    clean = re.sub('</Am\d>', '</hi>', clean)
    clean = re.sub('<INI\d>', '', clean)
    clean = re.sub('</INI\d>', '', clean)
    clean = clean.replace('<P>','<p>')
    clean = clean.replace('</P>', '</p>')
    clean = clean.replace("^&", "&amp;")
    clean = re.sub('<lb n=".*?"/><konghang.*?>', '', clean)
    clean = clean.replace('<P/><p>', '<O/>')
    clean = clean.replace('</p><P/>', '<C/>')
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
    clean = clean.replace('<hi rend="italic"></hi>', '')
    clean = clean.replace('<hong>','')
    clean = clean.replace('</hong>','')
    clean = clean.replace('<hi rend="italic">;</hi>', ';')
    clean = clean.replace('<hi rend="italic">:</hi>', ':')
    clean = clean.replace('<hi rend="italic">!</hi>', '!')
    clean = clean.replace('<hi rend="italic">?</hi>', '?')
    clean = clean.replace('<tspb>', '')
    clean = clean.replace('</tspb>', '')
    clean = clean.replace('<shi>','<p>')
    clean = clean.replace('</shi>','</p>')
    clean = clean.replace('<yinfu/>','')
    clean = clean.replace('{et}', '&amp;')
    clean = clean.replace('</hi> &amp; <hi rend="italic">', ' &amp; ')
    clean = clean.replace('<DUAN>','')
    clean = clean.replace('</DUAN>','')
    #delete empy lines
    clean = [line for line in clean.split('\n') if line.strip() != '']
    clean = '\n'.join(clean)
    return clean

'''find a footnote-end and add a </note>'''

def find_foot(file):
    file=file.split('\n')
    new=[]
    newest=[]
    for number, line in enumerate(file):
        if '<note type="footnote">' in line:
            for i in range(number+2,number+34):
                if file[i].startswith('<pb') or file[i].startswith('<body>'):
                    x=i-1
                    new.append(file[x])
                    newest.append(file[x]+'</note>')
                    break
    return new, newest


'''in the case of multipagefootnotes: </FO>-for footnote-beginning'''

def find_foot2(file):
    file = file.split('\n')
    new=[]
    newest=[]
    for number, line in enumerate(file):
        if '<note type="footnote">' in line:
            next_line=file[number+1]
            if '<O/>' in next_line:
                new.append(next_line)
                new_line=next_line.replace('<O/>','<FO/><p>')
                newest.append(new_line)
    return new, newest


'''in the case of multipagefootnotes: </FC>-for footnote-end'''

def find_tail(file):
    file = file.split('\n')
    tail = []
    new_tail = []
    for number, line in enumerate(file):
        if '</note>' in line:
            if '<C/>' in line:
                tail.append(line)
                new_l=line.replace('<C/>','<FC/></p>')
                new_tail.append(new_l)
    return tail,new_tail


def replacement(old_data, new_data, file):
    for index, replaced_word in enumerate(old_data):
        file = file.replace(replaced_word, new_data[index])
    return file


def main():
    for document in glob.glob("C:/Users/yulya/PycharmProjects/TEI-XML/Roman_korrigiert/*.xml"):
        changed=changing(document)
        foot=find_foot(changed)
        right_place=replacement(foot[0],foot[1],changed)
        right_place=right_place.replace('</front></note>','</note></front>')
        footed = find_foot2(right_place)
        footed2 = find_tail(right_place)
        right_place = replacement(footed[0],footed[1],right_place)
        right_place = replacement(footed2[0],footed2[1],right_place)
        #save new file in the new folder, saving its name
        save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/ocr-xmls/'
        name = os.path.basename(document)
        fullname = os.path.join(save_path, name)
        fa = open(fullname, 'w', encoding="utf8")
        fa.write(right_place)
        fa.close


if __name__ == "__main__":
    main()





