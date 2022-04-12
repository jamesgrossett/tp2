
import socket
import sys
from time import sleep
import random
from struct import pack

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#host, port = '10.0.0.52', 65000 #Home address
host, port = '10.89.209.82', 65000 #UQ address
server_address = (host, port)

# Send message every 1 second
while True:

    # Generate random integer between 0, 100 and send
    inventory, errorState, bluetoothStatus, wifiStatus = random.randint(0, 100), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)
    message = pack('1H2?', inventory, errorState, bluetoothStatus)
    sock.sendto(message, server_address)

    sleep(1)