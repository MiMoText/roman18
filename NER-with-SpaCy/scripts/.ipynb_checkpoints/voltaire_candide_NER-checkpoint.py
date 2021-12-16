import spacy
from spacy import pipeline
from spacy import morphology
import fr_core_news_md

# ACHTUNG! Es ist wichtig spacy 2.3.0 installiert zu haben. Spacy 2.3.1 hat einen Bug im französischen Sprachmodell.
# Vorab einmal Download der Sprachmodelle notwendig, dazu untenstehende Befehle in Terminal ausführen. Danach können diese mit "load" geladen werden
# python -m spacy download fr_core_news_md

# Sprachmodell wird geladen
nlp = fr_core_news_md.load()

# Hier Dateinamen ersetzen

with open("../../plain/files/voltaire_candide.txt", encoding="utf-8") as file:
    text = file.read()
print(text)

doc = nlp(text)

for entity in doc.ents:
    print(entity.text, entity.label_)
