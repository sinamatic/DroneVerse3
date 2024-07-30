# Sina Steinmüller
# Stand: 2024-06-30
"""
This program reads the gyroscope values from the OSC server and calculates the direction of the movement based on the average values of the last 500 values.
"""

import argparse
from collections import deque
from pythonosc import dispatcher as osc_dispatcher_module
from pythonosc import osc_server
import threading
import pygame
import sys

# Faktoren zur Anpassung der Gyro-Werte für bessere Sichtbarkeit der Neigung
GYRO_FACTOR = 100.0  # Multiplikationsfaktor für bessere Lesbarkeit
HISTORY_SIZE = 500  # Anzahl der Werte zur Berechnung der Richtung


# Funktion zur Berechnung der Richtung basierend auf Durchschnittswerten
def determine_direction(gyro_x_values, gyro_y_values, gyro_z_values):
    # Kombiniere die Gyrowerte in eine Liste von Tupeln
    gyro_values = list(zip(gyro_x_values, gyro_y_values, gyro_z_values))

    # Initialisiere Summen für x, y und z
    sum_x, sum_y, sum_z = 0, 0, 0

    for x, y, z in gyro_values:
        sum_x += x
        sum_y += y
        sum_z += z

    # Berechne den Durchschnitt
    avg_x = sum_x / HISTORY_SIZE
    avg_y = sum_y / HISTORY_SIZE
    avg_z = sum_z / HISTORY_SIZE

    # Bestimme die größte durchschnittliche absolute Bewegung
    max_value = max(abs(avg_x), abs(avg_y), abs(avg_z))

    # Bestimme die Richtung basierend auf dem größten Wert
    if max_value == abs(avg_x):
        if avg_x > 0:
            return "right"
        else:
            return "left"
    elif max_value == abs(avg_y):
        if avg_y > 0:
            return "down"
        else:
            return "up"
    elif max_value == abs(avg_z):
        if avg_z > 0:
            return "forward"
        else:
            return "backward"


def format_osc_value(value, factor):
    return format(value * factor, ".0f")  # Formattierung ohne Nachkommastelle


def run_osc_detection(direction_callback):
    direction = "none"

    print("OSC-Detection gestartet")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        default="192.168.50.152",  # lisas router
        help="Die IP-Adresse, auf der der OSC-Server lauschen soll",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5005,
        help="Der Port, auf dem der OSC-Server lauschen soll",
    )
    args = parser.parse_args()

    # Initialisierung der Variablen für die Gyro-Werte
    gyro_x_values = deque(maxlen=HISTORY_SIZE)
    gyro_y_values = deque(maxlen=HISTORY_SIZE)
    gyro_z_values = deque(maxlen=HISTORY_SIZE)

    def update_direction():
        nonlocal direction
        if (
            len(gyro_x_values) == HISTORY_SIZE
            and len(gyro_y_values) == HISTORY_SIZE
            and len(gyro_z_values) == HISTORY_SIZE
        ):
            direction = determine_direction(gyro_x_values, gyro_y_values, gyro_z_values)
            direction_callback(direction)

    def gyro_handler_x(unused_addr, gyro_value):
        gyro_x_values.append(gyro_value)
        update_direction()

    def gyro_handler_y(unused_addr, gyro_value):
        gyro_y_values.append(gyro_value)
        update_direction()

    def gyro_handler_z(unused_addr, gyro_value):
        gyro_z_values.append(gyro_value)
        update_direction()

    osc_dispatcher = osc_dispatcher_module.Dispatcher()
    osc_dispatcher.map("/data/motion/gyroscope/x", gyro_handler_x)
    osc_dispatcher.map("/data/motion/gyroscope/y", gyro_handler_y)
    osc_dispatcher.map("/data/motion/gyroscope/z", gyro_handler_z)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), osc_dispatcher)
    print(f"OSC-Server gestartet auf {args.ip}:{args.port}")

    # Pygame initialisieren und Bildschirm erstellen
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("OSC Detection")
    clock = pygame.time.Clock()

    # Hintergrundbild laden und skalieren
    background_image = pygame.image.load("images/DSC01497.jpg")
    background_image = pygame.transform.scale(background_image, (1920, 1080))

    # Schriftarten und -größen definieren
    font_large = pygame.font.SysFont("Arial", 80, bold=True)
    font_medium = pygame.font.SysFont("Arial", 72)
    font_small = pygame.font.SysFont("Arial", 48)
    font_textblock = pygame.font.SysFont("Arial", 24)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    # Überwache die Tasteneingabe für das Beenden des Programms
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    break

        screen.blit(background_image, (0, 0))

        # Überschriften zeichnen
        text_surface = font_large.render("DRONEVERSE", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(960, 65))
        screen.blit(text_surface, text_rect)

        text_surface = font_small.render(
            "You choose OSC/phone control.", True, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(center=(960, 150))
        screen.blit(text_surface, text_rect)

        # OSC-Ausgabe zeichnen
        text_surface = font_large.render(direction.upper(), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(960, 400))
        screen.blit(text_surface, text_rect)

        instructions = [
            "iPhone als Fernbedienung: Display schaut nach oben, Kamera nach links, Homebutton nach rechts.",
            "Drehung vom 45° nach rechts/links = forward, backward",
            "Kippbewegung nach links / rechts = left, right",
            "Kippbewegung nach oben / unten = up, down",
            "iPhone liegt still  = stop",
        ]
        text_y = 780  # Startposition Y für den Textblock
        for line in instructions:
            text_surface = font_textblock.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(960, text_y))
            screen.blit(text_surface, text_rect)
            text_y += 30  # Abstand zwischen den Zeilen

        pygame.display.flip()
        clock.tick(60)

    # Stoppe den OSC-Server und beende das Programm
    print("Beende OSC-Detection...")
    server.shutdown()
    server_thread.join()
    pygame.quit()
    # sys.exit()


if __name__ == "__main__":
    run_osc_detection(lambda direction: print(f"oscdetection.py sagt {direction}"))
