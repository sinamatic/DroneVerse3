# Sina Steinmüller
# Stand: 2024-06-25
# Liest Gyroskop Werte von der Data OSC App am iPhone ein
# Überträgt die Werte über IP im selben WLAN aufs Macbook
# Gibt X, Y und Z Werte auf der Konsole aus
# ToDo: Werte an die Drohne senden; Filterung der Werte

import argparse
from collections import deque
from pythonosc import dispatcher as osc_dispatcher_module
from pythonosc import osc_server

# Faktoren zur Anpassung der Gyro-Werte für bessere Sichtbarkeit der Neigung
GYRO_FACTOR = 100.0  # Multiplikationsfaktor für bessere Lesbarkeit
HISTORY_SIZE = 100  # Anzahl der Werte zur Berechnung


# Funktion zur Berechnung der Richtung basierend auf Durchschnittswerten
def calculate_direction(gyro_x_values, gyro_y_values, gyro_z_values):
    # Toleranzschwelle zur Erkennung der Bewegung
    TOLERANCE = 1.0

    avg_gyro_x = sum(gyro_x_values) / len(gyro_x_values)
    avg_gyro_y = sum(gyro_y_values) / len(gyro_y_values)
    avg_gyro_z = sum(gyro_z_values) / len(gyro_z_values)

    if abs(avg_gyro_x) > TOLERANCE:
        if avg_gyro_x > 0:
            return "right"
        else:
            return "left"
    elif abs(avg_gyro_y) > TOLERANCE:
        if avg_gyro_y > 0:
            return "up"
        else:
            return "down"
    elif abs(avg_gyro_z) > TOLERANCE:
        if avg_gyro_z > 0:
            return "forward"
        else:
            return "backward"
    else:
        return "none"


def format_osc_value(value, factor):
    return format(value * factor, ".0f")  # Formattierung ohne Nachkommastelle


def run_osc_detection(direction_callback):
    direction = "none"

    print("OSC-Detection gestartet")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        # ip address of the computer, change if necessary
        default=input("Gib die IP-Adresse ein (Standard: 192.168.178.44): ")
        or "192.168.178.44",  # sinas macbook
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

    def print_gyro_values():
        if gyro_x_values and gyro_y_values and gyro_z_values:
            formatted_x = format_osc_value(gyro_x_values[-1], GYRO_FACTOR)
            formatted_y = format_osc_value(gyro_y_values[-1], GYRO_FACTOR)
            formatted_z = format_osc_value(gyro_z_values[-1], GYRO_FACTOR)
            print(f"X: {formatted_x}\t|\tY: {formatted_y}\t|\tZ: {formatted_z}")

    def update_direction():
        nonlocal direction
        if (
            len(gyro_x_values) == HISTORY_SIZE
            and len(gyro_y_values) == HISTORY_SIZE
            and len(gyro_z_values) == HISTORY_SIZE
        ):
            direction = calculate_direction(gyro_x_values, gyro_y_values, gyro_z_values)
            direction_callback(direction)

    def gyro_handler_x(unused_addr, gyro_value):
        gyro_x_values.append(gyro_value)
        # print_gyro_values()
        update_direction()

    def gyro_handler_y(unused_addr, gyro_value):
        gyro_y_values.append(gyro_value)
        # print_gyro_values()
        update_direction()

    def gyro_handler_z(unused_addr, gyro_value):
        gyro_z_values.append(gyro_value)
        # print_gyro_values()
        update_direction()

    osc_dispatcher = osc_dispatcher_module.Dispatcher()
    osc_dispatcher.map("/data/motion/gyroscope/x", gyro_handler_x)
    osc_dispatcher.map("/data/motion/gyroscope/y", gyro_handler_y)
    osc_dispatcher.map("/data/motion/gyroscope/z", gyro_handler_z)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), osc_dispatcher)
    print(f"OSC-Server gestartet auf {args.ip}:{args.port}")

    server.serve_forever()


if __name__ == "__main__":
    # callback funktion
    run_osc_detection(lambda direction: print(f"oscdetection.py sagt {direction}"))
