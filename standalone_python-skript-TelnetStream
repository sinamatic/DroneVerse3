# Author: Tobias Schwarz
#Stand: 20.08.2024

# import keyboard
# import time
import telnetlib
import threading
import pygame

# 192.168.50.131 old IP Adresss
HOST = "192.168.50.33"  # Adresse des Telnet-Servers
PORT = 23  # Standard-Telnet-Port
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
            # Wenn Fenster geschlossen
            run = False
            tn.close()
            print("Telnet-Verbindung geschlossen. Programm beendet.")
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            # Wenn Taste gedrückt
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
            # Wenn Taste losgelassen
            tn.write("x".encode('ascii') + b"\n") 
            print("stop")

# </pygame>______________________________________________________________

def write(char):
    tn.write(char)

def listen_to_server():
    while True:
        try:
            # Liest Nachrichten vom Server
            message = tn.read_very_eager()
            if message:
                print(">>> Nachricht vom Server:", message.decode('ascii'))
        except Exception as e:
            print(f"Fehler beim Empfangen der Nachricht: {e}")
            break

# Startet Listener in separatem Thread
thread = threading.Thread(target=listen_to_server)
thread.daemon = True
thread.start()
