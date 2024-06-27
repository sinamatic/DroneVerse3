# Usage main.py

zum reinen Testen der Gestenerkennung:
bool `test_with_drone` = False setzen. Fürs testen mit Drohne: True setzen.

# testmain.py

Modularisierte Version von main.py mit Modulen für die Gestenerkennung und die Drohensteuerung, damit Gestenerkennung einfach austauschbar wird.

Gestenerkennung nur bei rechter Hand, linke Hand wird ignoriert.

# ToDo

- Keyboard Control von testmain.py auslagern in keyboarddetection.py
- dronecontrol.py mit tello funktionen versehen, vgl. main,py

## testmain.py

- alles was gestenerkennung ist auslagern in gestenerkennung
- 3 steuerungsoptionen einbauen: gesten, handy, keyboard
- gestenerkennung langsamer als in main.py, warum ???

# OSC Control

Für Applenutzer (iPhone, Macbook)

- Download von Data OSC
- Rausfinden der eigenen Computer IP Adresse (Apple: Systemeinstellungen, WLAN auswählen, Details … )
- Eingabe der eigenen IP Adresse in Data OSC, Port 5005
- Anpassung der IP im Code osc_control
- aktivieren von "Motion / Gyroscope werten
