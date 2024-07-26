# Sina Steinmüller
# Stand: 2024-07-26

""" 
Main program that starts the chosen detection and control modules based on the user's choice.
"""

# main.py

# import detection modules
# main.py
# import pygame
import logging
import time
from collections import defaultdict


# import detection modules
from gesturedetection import run_gesture_detection
from oscdetection import run_osc_detection
from keyboarddetection import run_keyboard_control
import userinterface

# import control modules
from print_dronecontrol import PrintDroneController
from tello_dronecontrol import TelloDroneController
from quadcopter_dronecontrol import QuadcopterDroneController
from tello_dronecontrol import Tello

# Choose between print and tello controller, check userinterface
chosen_detection = None
chosen_control = None
drone_controller = None

# pygame.init()
# clock = pygame.time.Clock()

# Timelogger for printing time in milliseconds
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)


signal_counts = defaultdict(int)
last_output_time = time.time()


def direction_from_gestures(direction):
    global signal_counts, last_output_time  # Deklariere Variablen als global

    # Hole die aktuelle Zeit
    current_time = time.time()
    current_second = int(current_time)
    # Zähle das Signal für die aktuelle Sekunde
    signal_counts[current_second] += 1

    # Logging der Information
    logging.info(
        f"{signal_counts[current_second]} Chosen Control: Gestures \t Direction from Control: {direction}"
    )

    # Prüfe, ob 60 Sekunden seit der letzten Ausgabe vergangen sind
    if current_time - last_output_time >= 60:
        last_output_time = current_time

    send_direction_to_drone(direction)


def direction_from_osc(direction):
    global signal_counts, last_output_time  # Deklariere Variablen als global

    # Hole die aktuelle Zeit
    current_time = time.time()
    current_second = int(current_time)
    # Zähle das Signal für die aktuelle Sekunde
    signal_counts[current_second] += 1

    # Logging der Information
    logging.info(
        f"{signal_counts[current_second]} Chosen Control: Phone \t Direction from Control: {direction}"
    )

    # Prüfe, ob 60 Sekunden seit der letzten Ausgabe vergangen sind
    if current_time - last_output_time >= 60:
        last_output_time = current_time
    send_direction_to_drone(direction)


def direction_from_keyboard(direction):
    global signal_counts, last_output_time  # Deklariere Variablen als global

    # Hole die aktuelle Zeit
    current_time = time.time()
    current_second = int(current_time)
    # Zähle das Signal für die aktuelle Sekunde
    signal_counts[current_second] += 1

    # Logging der Information
    logging.info(
        f"{signal_counts[current_second]} Chosen Control: Keyboard \t Direction from Control: {direction}"
    )

    # Prüfe, ob 60 Sekunden seit der letzten Ausgabe vergangen sind
    if current_time - last_output_time >= 60:
        last_output_time = current_time
    send_direction_to_drone(direction)


# Funktion zur Weiterleitung der Richtung an dronecontrol.py
def send_direction_to_drone(direction):
    global drone_controller

    if direction == "up":
        drone_controller.up()
    elif direction == "down":
        drone_controller.down()
    elif direction == "left":
        drone_controller.left()
    elif direction == "right":
        drone_controller.right()
    elif direction == "forward":
        drone_controller.forward()
    elif direction == "backward":
        drone_controller.backward()
    elif direction == "yaw_left":
        drone_controller.yaw_left()
    elif direction == "yaw_right":
        drone_controller.yaw_right()
    elif direction == "stop":
        drone_controller.stop()
    else:
        print(f"Invalid direction: {direction}")


if __name__ == "__main__":
    chosen_detection, chosen_control = userinterface.get_user_choices()

    print(f"Chosen Detection: {chosen_detection}")
    print(f"Chosen Control: {chosen_control}")

    if chosen_control == "tello":
        drone_controller = TelloDroneController()
    elif chosen_control == "quadcopter":
        drone_controller = QuadcopterDroneController()
    elif chosen_control == "print":
        drone_controller = PrintDroneController()
    else:
        print("Invalid control method.")

    if chosen_detection == "keyboard":
        run_keyboard_control(direction_from_keyboard)
    elif chosen_detection == "osc":
        run_osc_detection(direction_from_osc)
    elif chosen_detection == "gesture":
        run_gesture_detection(direction_from_gestures)
    else:
        print("Invalid detection method.")
