# Sina Steinmüller
# Stand: 2024-06-30
""" 
This program provides a simple Tello drone controller for demonstration purposes.
Needs to be updated, not tested yet.
"""
from djitellopy import Tello


class TelloDroneController:
    def __init__(self):
        drone = Tello()
        print("Drone initialized.")
        drone.connect()
        print("Drone connected.")
        drone.streamoff()
        drone.streamon()
        pass

    def drone_up(self):
        print("Tello: Up")

    def drone_down(self):
        print("Tello: down")

    def drone_left(self):
        print("Tello: left")

    def drone_right(self):
        print("Tello: right")

    def drone_forward(self):
        print("Tello: forward")

    def drone_backward(self):
        print("Tello: backward")
