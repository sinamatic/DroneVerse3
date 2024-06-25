import argparse
from pythonosc import dispatcher
from pythonosc import osc_server


def handle_osc_message(address, *args):
    # Hier kannst du den Code einfügen, um die empfangenen OSC-Nachrichten zu verarbeiten
    print(f"Empfangene OSC-Nachricht: {address} {args}")


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
    dispatcher.set_default_handler(handle_osc_message)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print(f"OSC-Server gestartet auf {args.ip}:{args.port}")

    server.serve_forever()
