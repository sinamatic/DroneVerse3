import argparse
from pythonosc import dispatcher
from pythonosc import osc_server


def receive_osc_data(address, *args):
    print(f"Empfangene Nachricht: {address} {args}")
    if len(args) > 0:
        try:
            gyro_value = float(args[0])
            print(f"Empfangener Gyroskop-Wert: {gyro_value}")

        except ValueError:
            print(f"Ungültiger Wert empfangen: {args[0]}")


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

    dispatcher = dispatcher.Dispatcher()
    # dispatcher.set_default_handler(receive_osc_data)
    dispatcher.map("/data/motion/gyroscope/x", receive_osc_data)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print(f"OSC-Server gestartet auf {args.ip}:{args.port}")

    server.serve_forever()
