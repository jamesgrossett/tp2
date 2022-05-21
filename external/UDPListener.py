import socket
import sys
from struct import unpack, pack

#UDP server address and port
HOST, PORT = '10.0.0.52', 65000 #Home address
#HOST, PORT = '10.89.210.83', 65000 #UQ Address

class Listener():
    def __init__(self):
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.settimeout(3) #Set socket to timeout after 3 seconds for socket operations
        # Bind the socket to the port
        self.address = (HOST, PORT)
        print(f'Starting UDP server on {HOST} port {PORT}')
        self.sock.bind(self.address)

    #Waits for message in form of key value pair to recieve, then returns it
    def recieve_keyvalue(self):
        # Try to recieve message
        try:
            message, self.address = self.sock.recvfrom(4096)
            print(f'Received {len(message)} bytes:')
            key, value = unpack('2H', message)
            return key, value
        # If socket times out - no connection or message recieved
        except:
            print('Failed to recieve data (timeout)')

    #Sends message in form of key value pair
    def send_keyvalue(self, key, value):
        message = pack('2H', key, value)
        self.sock.sendto(message, self.address)