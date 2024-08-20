from djitellopy import Tello, tello
import time


class TelloDroneController:

    def __init__(self):

        self.drone = Tello()
        print("Drone initialized.")

        # Geschwindigkeiten der Drohne werden auf 0 initialisiert
        self.speed_left_right = 0
        self.speed_up_down = 0
        self.speed_forward_back = 0
        self.yaw_speed = 0

        self.drone.connect()
        print("Drone connected.")

        self.takeoff()  # Drohne hebt ab

        self.speed = 30  # Geschwindigkeit der Drohne

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
