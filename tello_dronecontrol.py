# Maximilian Richter
# Sina Steinmüller
# Stand: 2024-07-26
""" 
This program provides a simple Tello drone controller for demonstration purposes.
Needs to be updated, not tested yet.
"""
from djitellopy import Tello
import time


class TelloDroneController:

    def __init__(self):
        self.drone = Tello()
        print("Drone initialized.")

        # Initialisiere Geschwindigkeiten
        self.speed_left_right = 0  # Links/Rechts
        self.speed_up_down = 0  # Auf/Ab
        self.speed_forward_back = 0  # Vorwärts/Rückwärts
        self.yaw_speed = 0  # Drehung

        self.drone.connect()
        print("Drone connected.")
        self.drone.streamoff()
        self.drone.streamon()

        self.takeoff()  # Drohne hebt ab, sobald die Instanz erstellt wird

        self.speed = 20  # Geschwindigkeit der Drohne

    def update_movement(self):
        self.drone.send_rc_control(
            self.speed_left_right,
            self.speed_forward_back,
            self.speed_up_down,
            self.yaw_speed,
        )

    def up(self):
        self.speed_up_down = self.speed
        self.update_movement()
        print("Tello: Up")

    def down(self):
        self.speed_up_down = -self.speed
        self.update_movement()
        print("Tello: Down")

    def left(self):
        self.speed_left_right = -self.speed
        self.update_movement()
        print("Tello: Left")

    def right(self):
        self.speed_left_right = self.speed
        self.update_movement()
        print("Tello: Right")

    def forward(self):
        self.speed_forward_back = self.speed
        self.update_movement()
        print("Tello: Forward")

    def backward(self):
        self.speed_forward_back = -self.speed
        self.update_movement()
        print("Tello: Backward")

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
        print("Tello: Stop")

    def land(self):
        self.drone.land()
        print("Tello: land")
