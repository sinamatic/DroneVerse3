# main.py

# import detection modules
from gesturedetection import run_gesture_detection
from oscdetection import run_osc_detection
from keyboarddetection import run_keyboard_control

# import control modules
from print_dronecontrol import PrintDroneController
from tello_dronecontrol import TelloDroneController

# choosen_detection = "gestures"  # Wähle die Gestenerkennung aus
# choosen_detection = "osc"  # Wähle die OSCerkennung aus
choosen_detection = "keyboard"  # Wähle die Tastaturerkennung aus

choosen_control = "print"  # Wähle die Druckausgabe aus
# choosen_control = "tello"  # Wähle die Tello-Steuerung aus


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

    # Choose between print and tello controller
    if choosen_control == "print":
        drone_controller = PrintDroneController()
    elif choosen_control == "tello":
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
    if choosen_detection == "gesture":
        run_gesture_detection(direction_from_gestures)
    elif choosen_detection == "osc":
        run_osc_detection(direction_from_osc)
    elif choosen_detection == "keyboard":
        run_keyboard_control(direction_from_keyboard)
    else:
        print("Ungültige Auswahl")
