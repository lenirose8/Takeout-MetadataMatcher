# Takeout-MetadataMatcher
Hallo, das hier ist ein einfaches Tool um die Metadaten aus eurem Google Takeout zu fixen. Es entnimmt die Metadaten aus der json Datei und integriert sie in eure normalen Bilder und Videos. Dann haben alle eure Dateien endlich wieder das richtige Datum!
Falls ihr gar keine Ahnung von Coden und Programmieren habt, ist das genau eure Anlaufstelle.

Hier eine Schritt für Schritt Anleitung.

1. Fragt auf der Google Taekout Seite eure Dateien an. Dann ladet ihr die Zip-Dateien herunter und -ganz wichtig- extrahiert sie (Doppelklick auf den Ordner der Zip-Datei und dann steht oberhalb in der Leiste "alle extrahieren"). Jetzt könnt ihr eure extrahierten Dateien noch wahlweise alle in einen großen Ornder sortieren oder nach Jahren sortieren, das ist gleich, solange die Dateien extrahiert wurden.
2. Ladet euch die neueste Version von Python für euer Betriebssystem herunter (ist inklusive Manager): https://www.python.org/downloads/
   (Falls ihr Python schon habt: Betriebssystem 3.10 oder neuer)
3. Ladet den kompletten Ordner oben mit allen Dateien herunter.
4. Installiert exiftool auf eurem Rechner. Das ist dazu da, um die Metadaten (also Datum usw.) in euren Dateien zu überschreiben: https://exiftool.org/
   
   Danach unzipped (also extrahiert) ihr auch den exiftool Ordner. Ihr habt jetzt also einen ausgepackten Ordner, indem mehrere Dateien sind. Eine Datei heißt
   "exiftool-(3).exe" oder so ähnlich, diese bennent ihr um in "exiftool.exe".
   <img width="853" height="117" alt="image" src="https://github.com/user-attachments/assets/c92e0ade-133b-428d-962c-d1a6e35c693c" />

   Den kompletten Ordner verschiebt ihr dann in den Takeout-MetadataMatcher Ordner. Das sollte dann so aussehen:
   <img width="788" height="317" alt="image" src="https://github.com/user-attachments/assets/33ec0c58-cbba-4614-9daf-bad872550480" />
5. Mini Code Anpassung: Geht in writer.py (Einmal anklicken, dann über Rechtsklick, Edit in IDLE, und neueste Python Version anklicken)
   <img width="823" height="698" alt="image" src="https://github.com/user-attachments/assets/54115bb8-9978-45f3-8e91-4d5e350ace27" />

   Jetzt müsst ihr nur eine kleine Zeile ändern, und zwar den Pfad, wo Ihr das Exiftool gespeichert habt. Ihr ersetzt das umrandete durch euren eigenen Pfad:
   EXIFTOOL_PATH = r"C:\Pfad\zu\exiftool.exe":
   <img width="826" height="847" alt="Screenshot 2026-07-05 202315" src="https://github.com/user-attachments/assets/9a87c76c-e2ec-483b-99c8-14f31f64a883" />

   Danach noch speichern (links oben: File --> save). Falls ihr das mit eurem Pfad nicht ganz versteht, fragt einfach mal chatgpt oder so ;)
6. SUPER! Wenn ihr es bis hierhin geschafft habt, ist der Rest ein Kinderspiel. Starte das Programm main.py.
   (Gibt mehrere Methoden zum Starten, am einfachsten ist Doppelklick, sonst einfach nochmal googeln, falls das Programm herumspinnt, wie man es profesionneller
   öffnet)
7. Wähle deinen Google Takeout Ordner aus. Ihr könnt auch erst mal einen Test-Ordner mit weniger Dateien zur Probe durchlaufen lassen. (Ich empfehle in jedem Fall dringend, vorher eine Sicherheitskopie zu machen, da die Originaldateien überschrieben werden.)
8. Auf "FULL RUN (EXIFTOOL)" klicken.
9. Warten, bis die Verarbeitung abgeschlossen ist. (Je nach Dateien Anzahl kann es Minuten bis mehrere Stunden dauern.)
10. Hoffentlich hat alles geklappt! Wenn nicht sorry, dann weiß ich auch nicht woran es liegt...





Weitere Infos:

Ein Python-Tool zum Wiederherstellen von Foto- und Videometadaten aus einem Google Takeout-Export.

Funktionen
Stellt Aufnahme- und Erstellungsdatum anhand der Google-Takeout-JSON-Dateien wieder her.
Unterstützt Bilder und Videos.
Erkennt auch verkürzte JSON-Dateinamen (z. B. .suppl.json oder abgeschnittene Varianten von supplemental-metadata.json).
Unterstützt den Sonderfall, dass eine HEIC- und eine MP4-Datei dieselbe JSON-Datei verwenden.
Protokolliert Fehler, ohne den gesamten Vorgang abzubrechen.
Zeigt während der Verarbeitung regelmäßig den Fortschritt an.

Unterstützte Dateiformate

Bilder
JPG / JPEG
PNG
HEIC
GIF
BMP
WEBP
TIFF

Videos
MP4
MOV
AVI
MKV
3GP
M4V

Fehlerprotokoll
Falls Dateien nicht verarbeitet werden können, werden sie in einer error_log.json dokumentiert.
Mögliche Ursachen sind beispielsweise:
beschädigte Dateien
fehlende oder beschädigte JSON-Dateien
von ExifTool nicht unterstützte Dateien
schreibgeschützte Dateien
Hinweise

Google Takeout verwendet leider nicht immer ein einheitliches Namensschema. Dieses Tool berücksichtigt unter anderem:
verkürzte JSON-Dateinamen
unterschiedliche Dateinamenslängen
UUID-Dateinamen
Screenshot-Dateien
den Sonderfall gemeinsamer HEIC-/MP4-Metadaten
Bekannte Einschränkungen
Manche beschädigten Dateien können nicht repariert werden.
Einige Messenger-Videos (z. B. einzelne WhatsApp-Videos) lassen sich aufgrund des Dateicontainers nicht vollständig überschreiben.
Das Tool verändert ausschließlich Metadaten. Der eigentliche Bild- oder Videoinhalt bleibt unverändert.

   

