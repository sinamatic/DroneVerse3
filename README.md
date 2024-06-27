# Usage

Gestenerkennung nur bei rechter Hand, linke Hand wird ignoriert.

# ToDo

- dronecontrol.py mit tello funktionen versehen und in main.py einbauen

## testmain.py

modul veraltet

# OSC Control

Für Applenutzer (iPhone, Macbook)

- Download von Data OSC
- Rausfinden der eigenen Computer IP Adresse (Apple: Systemeinstellungen, WLAN auswählen, Details … )
- Eingabe der eigenen IP Adresse in Data OSC, Port 5005
- Anpassung der IP im Code osc_control, Eingabefeld öffnet bei Start der App
- aktivieren von "Motion / Gyroscope werten

Man bekommt 3 Achsen, X, Y und Z
x: links / rechts
y: hoch / runter
z: vorwärts / rückwärts

## Steuerung

iPhone mit Display nach oben halten, Kamera auf der Linken Seite, Homebutton auf der rechten Seite.

- Rechte iPhone Seite (Homebutton) nach unten kippen: right
- Linke iPhone Seite (Kamera) nach unten kippen: left
- Vordere Längskante nach unten kippen: down
- Hintere Längskante nach unten kippen: up
- iPhone gerade halten (Display oben) und gegen Uhrzeigersinn drehen: forward
- iPhone gerade halten (Display oben) und im Uhrzeigersinn drehen: backward
