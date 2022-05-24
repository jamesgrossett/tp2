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
                print(f'Received {len(data)} bytes:')
                data_decoded = data.decode('UTF-8')
                key = int(data_decoded[0])
                value = int(data_decoded[1] + data_decoded[2])
                return key, value
        except:
            print("Failed to recieve data (timeout)")