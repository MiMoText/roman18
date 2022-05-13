import os.path
import glob
import re


#set a path where your data are saved
path = "C:/Users/Probst\Documents/Arbeiten/MiMoText/01_Aufgaben und Projekte/02_Erweiterung des Korpus um weitere Werke/#393_Umwandlungen Frantext-Werke/01_Originalwerke/*.xml"
#set a path where you want to save your data
save_path = "C:/Users/Probst\Documents/Arbeiten/MiMoText/01_Aufgaben und Projekte/02_Erweiterung des Korpus um weitere Werke/#393_Umwandlungen Frantext-Werke/02_XML_roh/"


if not os.path.exists(save_path):
    os.makedirs(save_path)


def edition(path, save_path):
    for file in glob.glob(path):
        # open and read file
        f = open(file, "r", encoding="utf8")
        r = f.read()
        # Funktionen:
        # Attribute 'pos' und 'lemma' entfernen:
        new = re.sub("' pos='\w*?\W*?\s*?\w*?\W*?\' lemma='\w*?\W*?\w*?\W*?\w*?\W*?\w*?\W*?\w*?\'/>", "", r)
        # Elementname '<x:wf' mit Attribut 'word' entfernen, sodass nur die Attributwerte des Attributes 'word'erhalten bleiben:
        new = re.sub("<x:wf word='", "", new)
        # Einfügen von einer Leerzeile nach dem ';', da einige Wörter im vorherigen Schritt mit ';' direkt aneinander gekettet wurden:
        new = re.sub(";", "; ", new)
        # Entfernen von unnötigen Leerzeichen vor den Satzzeichen:
        new = re.sub(" :", ":", new)
        new = re.sub(" ;", ";", new)
        new = re.sub(" !", "!", new)
        new = re.sub(" \?", "?", new)
        # Entfernen der <pb>-Elemente:
        new = re.sub("<pb n='\d*?'/>", "", new)
        # Entfernen der <lb>-Elemente:
        new = re.sub("<lb/>", " ", new)
        # Ersetzten der <div>-Elemente durch <div>-Elemente mit dem Attribut 'chapter':
        new = re.sub("<div>", "<div type='chapter'>", new) 
        # Entfernen des TEI-Headers von frantext: 
        new = re.sub("<TEI xmlns:x='http://www.atilf.fr/allegro' xmlns='http://www.tei-c.org/ns/1.0'> <teiHeader> <fileDesc> <titleStmt> <title></title> <author> </author> </titleStmt> <publicationStmt> <idno type='FRANTEXT'></idno> <distributor> </distributor> <address> <addrLine> </addrLine> <addrLine> </addrLine> <addrLine> </addrLine> <addrLine></addrLine> </address> <availability status='free'> <p> </p> </availability> </publicationStmt> <sourceDesc> <biblStruct> <monogr> <imprint> <publisher> </publisher> </imprint> </monogr> </biblStruct> </sourceDesc> </fileDesc> <profileDesc> <creation> <date></date> </creation> </profileDesc> </teiHeader>", "", new)   
        #automatic generate filename
        name = os.path.basename(file)
        fullname = os.path.join(save_path, name)
        #write text to file
        fa = open(fullname, 'w', encoding="utf8")
        fa.write(new)


def main():
    edition(path, save_path)


main()
        
        