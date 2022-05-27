import socket
from struct import pack, unpack
from tkinter import E

BTaddress = '0c:96:e6:b5:0f:bc' #Laptop bluetooth MAC address
port = 6
backlog = 1
size = 1024

class BluetoothListener():
    def __init__(self):
        self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        print(f'Initialising Bluetooth host on mac address: {BTaddress} port {port}')
        self.sock.bind((BTaddress, port))
        self.sock.listen(backlog)
        #self.sock.settimeout(3)
        self.BTconnect()

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
            data = self.client.recv(size)
            if data:
                data_decoded = data.decode('UTF-8')
                print(f'Received {len(data)} bytes: {data_decoded}')
                key = int(data_decoded[0])
                value = int(data_decoded[1] + data_decoded[2])
                return key, value
        except:
            print("Failed to recieve data (timeout)")
    
    def send_keyvalue(self, key, value):
        #Account for value cases where value is <10 (single digit) by adding leading 0. Ignoring cases where value is >99 (triple digit) because this should not ever occur in reality
        if len(str(value)) == 1:
            value = '0' + str(value)
        
        message = format("%s%s" % (key, value))
        print("Sending: %s" % message)
        try:
            self.client.send(bytes(message, 'UTF-8'))
        except Exception as e:
            print('Message failed to send: ' + str(e))