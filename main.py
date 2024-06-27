# main.py

# import detection modules
from gesturedetection import run_gesture_detection
from oscdetection import run_osc_detection
from keyboarddetection import run_keyboard_control

# import control modules
from print_dronecontrol import PrintDroneController
from tello_dronecontrol import TelloDroneController

# Globale Variablen für die Auswahl
# chosen_detection = None
# chosen_control = None

# Choose between gesture, osc and keyboard detection
# chosen_detection = "gestures"
chosen_detection = "osc"
# chosen_detection = "keyboard"

# Choose between print and tello controller
chosen_control = "print"
# chosen_control = "tello"


def direction_from_gestures(direction):
    print(f"Chosen Control: Gestures \t Direction from Control: {direction}")
    send_direction_to_drone(direction)


def direction_from_osc(direction):
    print(f"Chosen Control: Phone \t Direction from Control: {direction}")
    send_direction_to_drone(direction)


def direction_from_keyboard(direction):
    print(f"Chosen Control: Keyboard \t Direction from Control: {direction}")
    send_direction_to_drone(direction)


# Funktion zur Weiterleitung der Richtung an dronecontrol.py
def send_direction_to_drone(direction):
    global chosen_control

    # Choose between print and tello controller
    if chosen_control == "print":
        drone_controller = PrintDroneController()
    elif chosen_control == "tello":
        drone_controller = TelloDroneController()

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
    else:
        print(f"Ungültige Richtung: {direction}")


if __name__ == "__main__":
    # import userinterface

    # Start user interface
    # userinterface.start_user_interface()

    if chosen_detection == "gesture":
        run_gesture_detection(direction_from_gestures)
    elif chosen_detection == "osc":
        run_osc_detection(direction_from_osc)
    elif chosen_detection == "keyboard":
        run_keyboard_control(direction_from_keyboard)
    else:
        print("Ungültige Auswahl")
