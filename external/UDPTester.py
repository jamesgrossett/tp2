import socket
import sys
from struct import unpack

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '10.0.0.52', 65000
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

while True:
    # Wait for message
    message, address = sock.recvfrom(4096)

    print(f'Received {len(message)} bytes:')
    x, = unpack('1f', message)
    print(x)

