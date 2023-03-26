import socket
from typing import Optional


def find_next_available_port(
    start_port: int = 5901, end_port: int = 5999, host="localhost"
) -> Optional[int]:
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                return port
            except OSError:
                continue
    return None
