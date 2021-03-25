import glob
import os.path

#read document

def line_reader(document):
    file = open(document, 'r', encoding='utf8')
    inhalt = file.readlines()
    inhalt_ = [line.strip() for line in inhalt]
    return inhalt_


''' find the hyphen at the end of a line and the end of the word at the next line 
to combine two parts of the word'''

def hyphen(inhalt):
    lines_new = []
    process = False
    process2 = False
    process3 = False
    process4 = False
    for number, line in enumerate(inhalt):
        if process:
            pos_first_word = inhalt[number].find(" ")
            line = line[pos_first_word+1:]
        elif process2:
            pos_second_word = inhalt[number].find(" ",2)
            line = line[pos_second_word+1:]
        elif process3:
            if line==inhalt[number]:
                line = line.replace(inhalt[number],' ')
        elif process4:
            pos_first_word = inhalt[number].find(" ")
            line = '<hi'+' '+ line[pos_first_word + 1:]
        try:
            if line[-1] == "-":
                next_line = inhalt[number + 1]
                pos_first_word = next_line.find(" ")
                first_word = next_line[:pos_first_word]
                pos_second_word = next_line.find(" ", 2)
                second_word = next_line[pos_first_word+1:pos_second_word]
                if next_line == first_word+'>':
                    line += first_word.replace('„','')+'>'
                    process = False
                    process2 = False
                    process3 = True
                    process4 = False
                elif next_line.startswith('<hi') or next_line.startswith('(<hi'):
                    pass
                    process = False
                    process2 = False
                    process3 = False
                    process4 = False
                elif first_word.endswith('<hi'):
                    first_word = first_word.replace('„','')
                    line +=first_word.replace('<hi','')
                    process = False
                    process2 = False
                    process3 = False
                    process4 = True
                elif first_word == '“':
                    line += second_word
                    process = False
                    process2 = True
                    process3 = False
                    process4 = False
                elif first_word.startswith('“'):
                    line += first_word.replace('“','')
                    process = True
                    process2 = False
                    process3 = False
                    process4 = False
                elif first_word.startswith('„'):
                    line += first_word.replace('„','')
                    process = True
                    process2 = False
                    process3 = False
                    process4 = False
                else:
                    line += first_word
                    process = True
                    process2 = False
                    process2 = False
                    process4 = False
            else:
                process = False
                process2 = False
                process3 = False
                process4 = False
            lines_new.append(line)
        except IndexError:
            pass
    text= [line for line in lines_new if line.strip() != '']
    text = '\n'.join(text)
    return text



def main():
    for document in glob.glob("C:/Users/yulya/PycharmProjects/TEI-XML/arbeitsxmls/*.xml" ):
        inhalt = line_reader(document)
        inhalt_neu = hyphen(inhalt)
        save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/xmls_for_plain1/'
        name = os.path.basename(document)
        fullname = os.path.join(save_path, name)
        fa = open(fullname, 'w', encoding="utf8")
        fa.write(inhalt_neu)
        fa.close


if __name__ == "__main__":
    main()