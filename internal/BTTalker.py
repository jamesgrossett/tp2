import socket
from struct import pack
from time import sleep

BTaddress = '0c:96:e6:b5:0f:bc' #Laptop bluetooth MAC address
port = 6
backlog = 1
size = 1024

class BluetoothTalker():
    def __init__(self):
        #Initialised bluetooth socket connection and connect to host
        self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.sock.connect((BTaddress, port))
        #self.attempt_connect(5)
        
        self.sock.settimeout(0.005)
        #self.BTconnect()

    #Sends a key-value pair to the bluetooth host
    def send_keyvalue(self, key, value):
        #Account for value cases where value is <10 (single digit) by adding leading 0. Ignoring cases where value is >99 (triple digit) because this should not ever occur in reality
        if len(str(value)) == 1:
            value = '0' + str(value)
        
        message = format("%s%s" % (key, value))
        print("Sending: %s" % message)
        try:
            self.sock.send(bytes(message, 'UTF-8'))
        except:
            print('Message failed to send (Host down?)')
    
    def BTconnect(self):
        try: 
            self.client, self.address = self.sock.accept()
            print('Successfully accepted connection')
        except socket.timeout:
            print('Connection timed out')
        except:
            print('Connection failed')
    
    def recieve_keyvalue(self):
        try:
            data = self.sock.recv(size)
            if data:
                print(f'Received {len(data)} bytes:')
                data_decoded = data.decode('UTF-8')
                key = int(data_decoded[0])
                value = int(data_decoded[1] + data_decoded[2])
                return key, value
        except:
            print("Failed to recieve data (timeout)")

    def attempt_connect(self, attempts):
        i = 0
        while (i < attempts):
            try:
                self.sock.connect((BTaddress, port))
            except Exception as e:
                print(f'Failed to connect: {e} | Attempt {i}')
                i+=1
                sleep(2)
        