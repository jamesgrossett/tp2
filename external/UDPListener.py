import socket
import sys
from struct import unpack

#UDP server address and port
HOST, PORT = '10.0.0.52', 65000

class Listener():
    def __init__(self):
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the port
        self.address = (HOST, PORT)
        print(f'Starting UDP server on {HOST} port {PORT}')
        self.sock.bind(self.address)

    #Waits for message to recieve, the returns it
    def recieve(self):
        # Wait for message
        message, self.address = self.sock.recvfrom(4096)

        print(f'Received {len(message)} bytes:')
        value, = unpack('1f', message)
        return value
