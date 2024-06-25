import argparse
from pythonosc import dispatcher
from pythonosc import osc_server

# Globale Variablen für die Mittelwertberechnung der Gyroskop-Werte
buf_count = 0
buf_gyro = 0


def handle_osc_message(address, *args):
    global buf_count, buf_gyro

    if len(args) > 0:
        try:
            gyro_value = float(
                args[0]
            )  # Annahme: Die empfangenen OSC-Nachrichten enthalten einen Gyroskop-Wert als erstes Argument

            # Zählt 10 Gyroskop-Werte zusammen
            if buf_count < 10:
                buf_gyro += gyro_value
                buf_count += 1
            else:
                gyro_value_mean = buf_gyro / 10  # Division durch 10
                print(f"Gemittelter Gyroskop-Wert: {gyro_value_mean}")
                buf_gyro = 0
                buf_count = 0

        except ValueError:
            print(f"Ungültiger Wert empfangen: {args[0]}")


# print(f"Empfangene OSC-Nachricht: {address} {args}")


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
