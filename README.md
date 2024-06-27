# Usage main.py

zum reinen Testen der Gestenerkennung:
bool `test_with_drone` = False setzen. Fürs testen mit Drohne: True setzen.

# testmain.py

Modularisierte Version von main.py mit Modulen für die Gestenerkennung und die Drohensteuerung, damit Gestenerkennung einfach austauschbar wird.

Gestenerkennung nur bei rechter Hand, linke Hand wird ignoriert.

# ToDo

- dronecontrol.py mit tello funktionen versehen und in main.py einbauen
- osccontrol.py berechnungen von links, rechts, oben und unten neu machen

## testmain.py

modul veraltet

# OSC Control

Für Applenutzer (iPhone, Macbook)

- Download von Data OSC
- Rausfinden der eigenen Computer IP Adresse (Apple: Systemeinstellungen, WLAN auswählen, Details … )
- Eingabe der eigenen IP Adresse in Data OSC, Port 5005
- Anpassung der IP im Code osc_control, Eingabefeld öffnet bei Start der App
- aktivieren von "Motion / Gyroscope werten
