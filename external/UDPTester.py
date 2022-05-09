import socket
import sys
from struct import unpack

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.settimeout(5)

# Bind the socket to the port
host, port = '10.0.0.52', 65000 #Home address
#host, port = '10.89.209.82', 65000 #UQ address
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

while True:
    # Wait for message
    try:
        message, address = sock.recvfrom(4096)
        print(f'Received {len(message)} bytes:')
        key, value = unpack('2H', message)
        print(key, value)
    except socket.timeout:
        print('Failed to recieve data (TIMEOUT)')
