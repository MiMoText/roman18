with open('Popeliniere_Daira_pl.xml', "r", encoding="utf8")as xml:        #open html document
    paragraph = xml.read()

paragraph = paragraph.replace('</p>', 'PARAGRAPH </p>')
print(paragraph)
f= open('paragr_Popeliniere_Daira_pl.xml', "w", encoding ='utf8')
f.write(paragraph)
f.close
