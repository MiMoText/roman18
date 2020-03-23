from bs4 import BeautifulSoup
import os.path
import glob


#read document
def file_reader(document):
    file = open(document, 'r', encoding='utf8')
    inhalt = file.read()
    return inhalt


def extraction(document):
    #delete linebreaks before and after footnotes
    doc = document.replace('</p>\n</note>', '</p></note>')
    doc = doc.replace('</hi>\n</p></note>', '</hi></p></note>')
    doc = doc.replace('</note> ','</note>')
    doc = doc.replace('<note type="footnote">\n<p>\n<hi', '<note type="footnote"><p><hi')
    #insert linebreak between paragraphs and heads>
    doc = doc.replace('</p> <p>','</p>\n<p>')
    doc = doc.replace(' <head>','\n<head>')
    doc = doc.replace('</head> ','</head>\n')
    return doc



def main():
    for file in glob.glob('C:/Users/yulya/PycharmProjects/TEI-XML/worksxmls/*.xml'):
        roman = file_reader(file)
        roman = extraction(roman)
        soup = BeautifulSoup(roman, "xml")
        #gives text without footnotes
        #for tag in soup.find_all('note'):
            #tag.extract()
        plain_text = soup.get_text()
        #gives text without <front> and <back>
        #plain_text = soup.body.get_text()
        #delete empty lines
        plain_text = [line for line in plain_text.split('\n') if line.strip() != '']
        plain_text = '\n'.join(plain_text)
        save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/texts/'
        name = os.path.basename(file)
        name = name.replace('xml','txt')
        fullname = os.path.join(save_path, name)
        print(plain_text)
        fa = open(fullname, 'w', encoding="utf8")
        fa.write(plain_text)


if __name__ == "__main__":
    main()