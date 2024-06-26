# Usage main.py

zum reinen Testen der Gestenerkennung:
bool `test_with_drone` = False setzen. Fürs testen mit Drohne: True setzen.

# testmain.py

Modularisierte Version von main.py mit Modulen für die Gestenerkennung und die Drohensteuerung, damit Gestenerkennung einfach austauschbar wird.

Gestenerkennung nur bei rechter Hand, linke Hand wird ignoriert.

# ToDo

- Simulation von Drohne überarbeiten, 3D Leinwand mit 3 Achsen, positionsaktualisierung der drohne im raum mit pygame ??
- Keyboard Control von testmain.py auslagern in keyboarddetection.py
- dronecontrol.py mit tello funktionen versehen, vgl. main,py

# OSC Control

Für Applenutzer (iPhone, Macbook)

- Download von Data OSC
- Rausfinden der eigenen Computer IP Adresse (Apple: Systemeinstellungen, WLAN auswählen, Details … )
- Eingabe der eigenen IP Adresse in Data OSC, Port 5005
- Anpassung der IP im Code osc_control
- aktivieren von "Motion / Gyroscope werten
