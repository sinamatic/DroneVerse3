# Author: Tobias Schwarz

""" 
This program provides a simple Tello drone controller for demonstration purposes.
Needs to be updated, not tested yet.
"""

# git add .
# git commit -m "nachricht"
# git push


import time
import telnetlib

HOST = "192.168.43.133"  # Adresse des Telnet-Servers
PORT = 23  # Standard-Telnet-Port
print("Connecting to Telnet server...")
tn = telnetlib.Telnet(HOST, PORT)  # Verbindung zum Telnet-Server herstellen
if not telnetlib.Telnet:
    print("Telnet-Verbindung konnte nicht hergestellt werden.")


class QuadcopterDroneController:

    def __init__(self):

        # print("Drone initialized.")

        # Initialisiere Geschwindigkeiten
        self.speed_left_right = 0  # Links/Rechts
        self.speed_up_down = 0  # Auf/Ab
        self.speed_forward_back = 0  # Vorwärts/Rückwärts
        self.yaw_speed = 0  # Drehung (bisher noch nicht implementiert)

        self.speed = 10  # Geschwindigkeit der Drohne

    def update_movement(self):
        self.speed_left_right,
        self.speed_forward_back,
        self.speed_up_down,
        self.yaw_speed

    # not in use
    def up(self):
        self.speed_up_down = self.speed
        self.update_movement()
        print("Tello: Up")

    # not in use
    def down(self):
        self.speed_up_down = -self.speed
        self.update_movement()
        print("Tello: Down")

    def left(self):
        if not testing:
            tn.write("a".encode("ascii") + b"\n")
        print("Quad: Left")

    def right(self):
        if not testing:
            tn.write("d".encode("ascii") + b"\n")
        print("Quad: Right")

    def forward(self):
        if not testing:
            tn.write("w".encode("ascii") + b"\n")
        print("Quad: Forward")

    # hier "nach oben" statt "zurück"
    def backward(self):
        if not testing:
            tn.write("s".encode("ascii") + b"\n")
        print("Quad: Backward")

    def takeoff(self):
        self.drone.takeoff()
        self.update_movement()
        print("Tello: Takeoff")

    def stop(self):
        # Setze alle Geschwindigkeiten auf 0, um die Drohne zu stoppen
        self.speed_left_right = 0
        self.speed_up_down = 0
        self.speed_forward_back = 0
        self.yaw_speed = 0
        self.update_movement()
        if not testing:
            tn.write("x".encode("ascii") + b"\n")
        print("Quad: Stop")

    # not in use
    def yaw_left(self):
        self.yaw_speed = -self.speed
        self.update_movement()
        print("Tello: Yaw Left")

    # not in use
    def yaw_right(self):
        self.yaw_speed = self.speed
        self.update_movement()
        print("Tello: Yaw Right")
