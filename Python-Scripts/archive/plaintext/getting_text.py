from bs4 import BeautifulSoup
import os.path
import glob

#type a path where your data are stored
data_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/worksxmls/*.xml'

# type a path where you want to save the text-data
save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/texts/'
if not os.path.exists(save_path):
    os.makedirs(save_path)



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


def parameter(document,cmd1,cmd2,cmd3):
    soup = BeautifulSoup(document, "xml")
    if cmd1 == 'NO':
        # gives text without footnotes
        for tag in soup.find_all('note'):
            tag.extract()
    else:
        pass
    if cmd2 == 'NO':
        # gives text without headings
        for tag in soup.find_all('head'):
            tag.extract()
    else:
        pass
    if cmd3 == 'body':
        # gives text without <front> and <back>
        plain_text = soup.body.get_text()
    if cmd3 == 'full':
        plain_text = soup.get_text()

    return plain_text


def main():
    cmd1 = input('please choose footnotes "YES|NO"')
    cmd2 = input('please choose headings "YES|NO"')
    cmd3 = input('please choose fullversion or just body "full|body"')
    for file in glob.glob(data_path):
        roman = file_reader(file)
        roman = extraction(roman)
        plaintext = parameter(roman,cmd1,cmd2,cmd3)
        #delete empty lines
        plaintext = [line for line in plaintext.split('\n') if line.strip() != '']
        plaintext = '\n'.join(plaintext)
        name = os.path.basename(file)
        name = name.replace('xml','txt')
        fullname = os.path.join(save_path, name)
        print(plaintext)
        fa = open(fullname, 'w', encoding="utf8")
        fa.write(plaintext)


if __name__ == "__main__":
    main()