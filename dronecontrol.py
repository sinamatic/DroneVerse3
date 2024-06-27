from djitellopy import Tello


# Funktion zur Initialisierung der Drohne
def initialize_drone():
    drone = Tello()
    print("Drone initialized.")
    drone.connect()
    print("Drone connected.")
    drone.streamoff()
    drone.streamon()
    return drone


test_with_drone = False

if test_with_drone:
    drone = initialize_drone()
    print("Drone initialized.")


def drone_up():
    print("Dronecontrol: Up")


def drone_down():
    print("Dronecontrol: down")


def drone_left():
    print("Dronecontrol: left")


def drone_right():
    print("Dronecontrol: right")


def drone_forward():
    print("Dronecontrol: forward")


def drone_backward():
    print("Dronecontrol: backward")
