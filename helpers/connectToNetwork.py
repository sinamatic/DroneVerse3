from djitellopy import tello

drone = tello.Tello()
drone.connect()
drone.connect_to_wifi("ASUS_90", "4391622734")  # ssid und passwort des Netzwerks
