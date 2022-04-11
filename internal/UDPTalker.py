
import socket
import sys
from time import sleep
import random
from struct import pack

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '10.0.0.52', 65000
server_address = (host, port)

# Send message every 1 second
while True:

    # Generate random integer between 0, 100 and send
    message = pack('f', random.randint(0, 100))
    sock.sendto(message, server_address)

    sleep(1)