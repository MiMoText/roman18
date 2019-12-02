# Workflow für die Transkription in XML-TEI mit TUSTEP und Python
## Hier wird der gesamte Workflow für die Transkription der Volltexte mit Python dokumentiert

### 1.Schritt: Die einzelnen RTF-Dateien zusammenzuführen (mithilfe von Tustep)

$$- SAMMELRTF.M:                 (last modified 2012.03.08 / MTr & KS)
$$- -----------
$$-
$$- Dieses Tuscript importiert die Daten aus mehreren RTF-Dateien
$$- aus einem beliebigen Verzeichnis in eine einzige (Tustep-Gesamt-)
$$- Zieldatei.
$$- ACHTUNG: Wenn diese schon existiert, wird sie angemeldet und vor
$$- dem Import gelöscht!
$$-
$$- Optional kann ein Muster vorgegeben werden, dem die Dateinamen
$$- entsprechen müssen (hier '*.rtf').
$$-
$$- Spezifikationen:
$$-
$$- PATH    = dirname     Der Namen des Verzeichnisses, in dem die
$$-                       RTF-Dateien stehen
$$- PATTERN = ...         Dateinamenmuster für die zu importierenden
$$-                       Dateien, z.B. *.rtf'text*.*
$$- ZIEL    = dateiname   Tustep-Ausgabedatei; wenn die Datei noch nicht
$$-                       existiert, wird sie kreiert; wenn sie schon
$$-                       existiert, wird sie überschrieben.
$$-
$$! path=D:\China-Erfassung\Sammel, pattern=*.rtf, ziel=julia5.tf
$$-
$$ MODE TUSCRIPT, {}

- Ggf. Verzeichnisname anfordern:

IF (path .EQ. "")  THEN
   ASK "Bitte Namen des Quellverzeichnisses angeben: ": path = ""
END IF

- Verzeichnisname prüfen:

SET path = CAPS (path) 
IF (path .NM. "|{&a}:\\*|")  THEN
   PRINT/ERROR "{path} : Laufwerksbuchstabe fehlt."
ELSE
   DEFINE/VOLUME dir = path
   IF ("dir" .NE. 'VOLUME')  THEN
      PRINT/ERROR "Verzeichnis {path} existiert nicht."
   END IF
   REMOVE/VOLUME dir
END IF

- Muster für Dateinamen prüfen:

IF (pattern .NE. "")  THEN
   CHECK R_TABLE/TEXT/OR fpos+fmld = ":{pattern}:"
   SET mld = CONCAT ("pattern: ", fmld)
   IF (fpos.NE.0)  ERROR/STOP mld
   BUILD R_TABLE/TEXT/OR pattern = ":{pattern}:"
END IF

- Zieldatei kreieren/anmelden und löschen::

ERROR/STOP CREATE (ziel, SEQ-O)
ERROR/STOP ERASE  (ziel)

- Ausführung (wobei COMPILE verwendet werden kann,
- aber keinen Geschwindigkeitsvorteil bringt):

SET files = FILE_NAMES (-, $path)
IF (pattern.NE."")  SET files = FILTER (files, pattern, -)
LOOP nr, file = files
   SET fullname = CONCAT (path, "\", file)
   DEFINE "qu*tmp.1" = fullname
   SET file = CAPS (file)
 ERROR/STOP OPEN ("qu*tmp.1", READ, -)
   IF ("qu*tmp.1" .EQ. 'FDF')  THEN
   PRINT/ERROR ""
   PRINT/ERROR "Datei Nr. ", nr, " (= ", file, ") wird importiert..."
   PRINT/ERROR ""
   EXECUTE #*import,qu*tmp.1,{ziel},ign=!font'size,lo=-
   END IF
   ERROR/STOP CLOSE ("qu*tmp.1")
   REMOVE "qu*tmp.1"
   - Nur zum Testen: Abbruch nach n importierten Dateien:
   - IF (nr .EQ. 8) STOP
END LOOP

### 2. Schritt: Die einzelnen RTF-Dateien den Romanen zuordnen und trennen (händisch)
### 3. Schritt: Bearbeitung mit TUSTEP, Erzeugung eines XML- Dokuments

1. Lesen die Datei mit dem Befehl sammelrtf.m ein (hier einen Pfad zur Datei eingeben). Immer nur eine Datei darf in dem Ordner liegen. TUSTEP sammelt die Datei ein und erzeugt eine TUSTEP-Datei. Sie wird separat gespeichert unter dem eingegeben Datei-Namen. (Ausführung: x, #makro,<editor>)
2. p_vorcod.p bearbeitet die erzeugte TUSTEP-Datei: Sonderzeichen werden ersetzt, eine XML-ähnliche Datei wird generiert (aber nicht wohlgeformt). Dateiname anpassen/eingeben. (Ausführung: x, #t, <editor>)
3. export_xml.p -exportiert die erzeugte XML-Datei. Dateiname anpassen/eingeben. (Ausführung: x, #t,<editor>)
   
   



