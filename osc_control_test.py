import argparse
from pythonosc import dispatcher
from pythonosc import osc_server

# Faktoren zur Anpassung der Gyro-Werte für bessere Sichtbarkeit der Neigung
GYRO_FACTOR = 10000.0  # Multiplikationsfaktor für bessere Lesbarkeit


def format_osc_value(value, factor):
    return format(value * factor, ".4f")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        default="192.168.178.44",
        help="Die IP-Adresse, auf der der OSC-Server lauschen soll",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5005,
        help="Der Port, auf dem der OSC-Server lauschen soll",
    )
    args = parser.parse_args()

    # Initialisierung der Variablen für die Gyro-Werte
    gyro_x = None
    gyro_y = None
    gyro_z = None

    def print_gyro_values():
        if gyro_x is not None and gyro_y is not None and gyro_z is not None:
            formatted_x = format_osc_value(gyro_x, GYRO_FACTOR)
            formatted_y = format_osc_value(gyro_y, GYRO_FACTOR)
            formatted_z = format_osc_value(gyro_z, GYRO_FACTOR)
            print(f"X: {formatted_x}\t|\tY: {formatted_y}\t|\tZ: {formatted_z}")

    def gyro_handler_x(unused_addr, gyro_value):
        global gyro_x
        gyro_x = gyro_value
        print_gyro_values()

    def gyro_handler_y(unused_addr, gyro_value):
        global gyro_y
        gyro_y = gyro_value
        print_gyro_values()

    def gyro_handler_z(unused_addr, gyro_value):
        global gyro_z
        gyro_z = gyro_value
        print_gyro_values()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/data/motion/gyroscope/x", gyro_handler_x)
    dispatcher.map("/data/motion/gyroscope/y", gyro_handler_y)
    dispatcher.map("/data/motion/gyroscope/z", gyro_handler_z)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print(f"OSC-Server gestartet auf {args.ip}:{args.port}")

    server.serve_forever()
