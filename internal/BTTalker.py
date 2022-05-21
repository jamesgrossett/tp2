import socket
from struct import pack
import random

BTaddress = '0c:96:e6:b5:0f:bc' #Laptop bluetooth MAC address
port = 6

class BluetoothTalker():
    def __init__(self):
        #Initialised bluetooth socket connection and connect to host
        self.s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.s.connect((BTaddress, port))

    #Sends a key-value pair to the bluetooth host
    def send_keyvalue(self, key, value):
        #Account for value cases where value is <10 (single digit) by adding leading 0. Ignoring cases where value is >99 (triple digit) because this should not ever occur in reality
        if len(str(value)) == 1:
            value = '0' + str(value)
        
        message = format("%s%s" % (key, value))
        print("Sending: %s" % message)
        try:
            self.s.send(bytes(message, 'UTF-8'))
        except:
            print('Message failed to send (Host down?)')


