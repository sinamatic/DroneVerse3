# print_dronecontrol.py


class PrintDroneController:
    def __init__(self):
        # Hier könntest du die Initialisierung der Drohnenverbindung oder andere Vorbereitungen vornehmen
        pass

    def up(self):
        print("DRONE GOES UP!", end="\r")

    def down(self):
        print("DRONE GOES DOWN!", end="\r")

    def left(self):
        print("DRONE GOES LEFT!", end="\r")

    def right(self):
        print("DRONE GOES RIGHT!", end="\r")

    def forward(self):
        print("DRONE GOES FORWARD!", end="\r")

    def backward(self):
        print("DRONE GOES BACKWARD!", end="\r")
