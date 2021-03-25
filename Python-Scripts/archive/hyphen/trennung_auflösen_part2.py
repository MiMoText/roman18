import glob
import os.path



def line_reader(document):
    file = open(document, 'r', encoding='utf8')
    inhalt = file.readlines()
    inhalt_ = [line.strip() for line in inhalt]
    return inhalt_


'''this script deals with hyphen at the end of a line, if there are xml-tags as well
here we have three different cases: with <hi>-element, line-breaks-</C> and both:<hi> and </C>
as input we take files from previous step: "trennung_auflösen". We took a big range for the case of linebreak, because 
it may occur, that we have footnotes at the and of a page with linebreak.'''

def hyphen_tags(inhalt):
    new_tail = []
    tail =[]
    old_tail =[]
    process = False
    for number, line in enumerate(inhalt):
        if process:
            line = inhalt[number].replace('<hi rend="italic">'+ word_tail, '')
        if '-<C/>' in line:
            for i in range(number+1,number+30):
                if inhalt[i].startswith('<O/>'):
                    word_suf = inhalt[i]
                    old_tail.append(word_suf)
                    word_tail = inhalt[i].split(' ')[0].replace('<O/>','')
                    new_line =word_suf.replace(word_tail+' ', '')
                    tail.append(new_line)
                    line = line.replace('<C/>','')+word_tail+'<C/>'
                    process= False
                    break
        if line.endswith('-</hi>'):
            next_line= inhalt[number+1]
            line = line.replace('-</hi>', '-')
            next_line = next_line.replace('<hi rend="italic">', '',1)
            word_tail = next_line.split(' ')[0]
            line = line+word_tail
            line = line.replace('</p></hi>','</hi></p>')
            process = True
        if line.endswith('-</hi><C/>'):
            print(line,inhalt[number+2])
            for i in range(number+1,number+10):
                if inhalt[i].startswith('<O/>'):
                    word_tail = inhalt[i].split(' ')[1].replace('rend="italic">','')
                    line = line.replace('</hi><C/>','')+word_tail+'<C/>'
                    #print(word_tail+str(number)+inhalt[1-10])
                    process = True

        new_tail.append(line)
    text = '\n'.join(new_tail)
    return old_tail,tail, text


def replacement(old_data, new_data, file):
    for index, replaced_word in enumerate(old_data):
        file = file.replace(replaced_word, new_data[index])
    return file


def main():
    for document in glob.glob("C:/Users/yulya/PycharmProjects/TEI-XML/xmls_for_plain1/*.xml" ):
        roman = line_reader(document)
        roman = hyphen_tags(roman)
        roman = replacement(roman[0], roman[1], roman[2])
        save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/xmls_for_plain2/'
        name = os.path.basename(document)
        fullname = os.path.join(save_path, name)
        fa = open(fullname, 'w', encoding="utf8")
        fa.write(roman)
        fa.close


if __name__ == "__main__":
    main()