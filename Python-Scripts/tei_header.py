
from bs4 import BeautifulSoup
import xmlformatter
import os.path
import glob
import string


'''this script adds the tei-header, sets the xml-id, number of words and size, formats xml,'''


path = 'C:/Users/yulya/PycharmProjects/TEI-XML/texts/*.txt'
save_path = 'C:/Users/yulya/PycharmProjects/TEI-XML/workxmls_formatted/'


#read files
def line_reader(document):
    file = open(document, 'r', encoding='utf8')
    inhalt = file.read()
    return inhalt


#count words in each document and save results as a dictionary
def count_words(path):
    dict = {}
    for file in glob.glob(path):
        text = open(file, 'r', encoding='utf8')
        text = text.read()
        #delete punctuation
        translator = str.maketrans('', '', string.punctuation)
        words= text.translate(translator)
        count = len(words.split())
        name = os.path.basename(file).replace('.txt','')
        dict[name] = count
    return dict


def header(file,dict,name):
    #converting to Beautifulsoup_object
    soup = BeautifulSoup(file, "xml")
    #navigation to TEI-element
    tag = soup.TEI
    # insert xml_id from document_ name
    tag['xml:id'] = name.replace('.xml', '')
    #
    for key in dict.keys():
        #filling out the number of words from previous funktion
        if key == name.replace('.xml', ''):
            tag2 = soup.extent.measure
            tag2.string.replace_with(str(dict[key]))
            #filling out information about size
            tag3 = soup.size
            if dict[key] < 50000:
                tag3['key'] = 'short'
            elif dict[key] > 50000 and dict[key] < 100000:
                tag3['key'] = 'medium'
            else:
                tag3['key'] = 'long'
            return soup



def main():
    dict = count_words(path)
    for file in glob.glob('C:/Users/yulya/PycharmProjects/TEI-XML/xmls_with_div/*.xml'):
        doc1 = line_reader('teiHeader-Template.xml')
        doc2 = line_reader(file)
        #combine header with text-body
        result = doc1 + doc2 + '</TEI>'
        #format
        #formatter = xmlformatter.Formatter(encoding_input="utf-8",encoding_output="utf-8")
        #formatted = formatter.format_string(result)
        #set file_name and save path
        name = os.path.basename(file)
        fullname = os.path.join(save_path, name)
        soup = header(result,dict,name)
        #save results
        fa = open(fullname, 'w', encoding="utf8")
        fa.write(str(soup))


if __name__ == "__main__":
    main()