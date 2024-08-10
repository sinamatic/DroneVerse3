# Author: Tobias Schwarz

import telnetlib
# import keyboard
import threading
# import time
import pygame

# Konfiguration
# 192.168.50.131
HOST = "192.168.50.33"  # Ersetze dies mit der Adresse deines Telnet-Servers
PORT = 23  # Standard-Telnet-Port, ändere dies entsprechend deiner Konfiguration
tn = telnetlib.Telnet(HOST, PORT) # Verbindung zum Telnet-Server herstellen

if not telnetlib.Telnet: print("Telnet-Verbindung konnte nicht hergestellt werden.")

# <pygame> _____________________________________________________________


pygame.init()
pygame.display.init()
pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()



run = True
while run:
    clock.tick(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            tn.close() # Schließe die Telnet-Verbindung 
            print("Telnet-Verbindung geschlossen. Programm beendet.")
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            # print(event)
            if event.key == pygame.K_a:
                print("left")
                tn.write("a".encode('ascii') + b"\n") 
            elif event.key == pygame.K_d:
                print("right")
                tn.write("d".encode('ascii') + b"\n") 
            elif event.key == pygame.K_w:
                print("front")
                tn.write("w".encode('ascii') + b"\n") 
            elif event.key == pygame.K_s:
                print("up")
                tn.write("s".encode('ascii') + b"\n") 
        elif event.type == pygame.KEYUP:
            tn.write("x".encode('ascii') + b"\n") 
            print("stop")


# variable wird im loop immmer größer und ab bestimmten wert wird erst wieder abgefragt




# </pygame>______________________________________________________________

def write(char):
    tn.write(char)

def listen_to_server():
    while True:
        try:
            # Lies die Nachricht vom Server
            message = tn.read_very_eager()
            if message:
                print(">>> Nachricht vom Server:", message.decode('ascii'))
        except Exception as e:
            print(f"Fehler beim Empfangen der Nachricht: {e}")
            break

# Starte den Listener in einem separaten Thread
thread = threading.Thread(target=listen_to_server)
thread.daemon = True  # Damit der Thread beendet wird, wenn das Hauptprogramm beendet wird
thread.start()
