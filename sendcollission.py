from pythonosc.udp_client import SimpleUDPClient


def send_osc_message(ip: str, port: int, message: str):
    client = SimpleUDPClient(ip, port)  # Create a UDP client
    client.send_message("/collision", message)  # Send the message


def run_send_collsion(danger):
    ip = "192.168.50.152"  # The IP address of the OSC server 192.168.50.152
    port = 8000  # The port number of the OSC server
    message = danger

    send_osc_message(ip, port, danger)
    print(f"Message '{danger}' sent to {ip}:{port}")


if _name_ == "_main_":
    run_send_collsion()
