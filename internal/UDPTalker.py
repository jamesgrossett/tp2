
import socket
import sys
from time import sleep
import random
from struct import pack

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '10.0.0.52', 65000 #Home address
#host, port = '10.89.209.82', 65000 #UQ address


class Talker():
    def __init__(self):
        self.server_address = (host, port)

    def send_keyvalue(self, key, value):
        message = pack('2H', key, value)
        sock.sendto(message, self.server_address)
