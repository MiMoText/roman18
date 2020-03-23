
from bs4 import BeautifulSoup
import xmlformatter
import os.path
import glob

'''this script adds the tei-header, sets the xml-id, formats xml and deletes unnecesary elements'''


#read files
def line_reader(document):
    file = open(document, 'r', encoding='utf8')
    inhalt = file.read()
    return inhalt




def main():
    for file in glob.glob('C:/Users/yulya/PycharmProjects/TEI-XML/xmls_for_plain3/*.xml'):
        doc1 = line_reader('teiHeader-Template.xml')
        doc2 = line_reader(file)
        #delete linebreaks
        doc2 = doc2.replace('\n',' ')
        #delete unnecesary elements
        doc2 = doc2.replace('<O/>','')
        doc2 = doc2.replace('<C/>','')
        #combine header with text-body
        result = doc1 + doc2 + '</TEI>'
        #format
        formatter = xmlformatter.Formatter(encoding_input="utf-8",encoding_output="utf-8")
        formatted = formatter.format_string(result)
        #converting to Beautifulsoup_object
        soup = BeautifulSoup(formatted, "xml")
        #set file_name and save path
        save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/worksxmls_formatted/'
        name = os.path.basename(file)
        fullname = os.path.join(save_path, name)
        #insert xml_id from document_ name
        tag = soup.TEI
        tag['xml:id'] = name.replace('.xml','')
        #save results
        fa = open(fullname, 'w', encoding="utf8")
        fa.write(str(soup))


if __name__ == "__main__":
    main()