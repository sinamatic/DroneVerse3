from pythonosc import dispatcher
from pythonosc import osc_server


def print_message(address, *args):
    print(f"Received message: {address} {args}")


def main():
    # Definiere den Dispatcher und die Callback-Funktion
    disp = dispatcher.Dispatcher()
    disp.set_default_handler(print_message)  # Handhabung aller eingehenden Nachrichten

    # Definiere die Adresse und den Port des Servers
    server = osc_server.ThreadingOSCUDPServer(("192.168.178.44", 5005), disp)
    print("Serving on port 5005")

    # Starte den Server
    server.serve_forever()


if __name__ == "__main__":
    main()
