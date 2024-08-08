# Lisa Berbig
# Stand: 2024-06-30

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading
import time

collision = None


def osc_handler(address, *args):
    global collision
    if args:
        collision = args[0]
        print(f"Collision value updated to: {collision}")


def run_osc_receiver(ip: str, port: int):
    dispatcher = Dispatcher()
    dispatcher.map("/collision", osc_handler)  # Map the specific address

    server = BlockingOSCUDPServer((ip, port), dispatcher)
    print(f"Starting OSC server on {ip}:{port}")

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    return server_thread


if __name__ == "_main_":
    ip = "127.0.0.1"  # Localhost, change as needed
    port = 8000  # Port number, change as needed

    server_thread = run_osc_receiver(ip, port)

    try:
        while True:
            if collision is not None:
                print(f"Current collision value: {collision}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server...")
