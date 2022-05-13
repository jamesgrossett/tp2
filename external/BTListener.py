import socket
from struct import pack, unpack

BTaddress = '0c:96:e6:b5:0f:bc' #Laptop bluetooth MAC address
port = 5
backlog = 1
size = 1024

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((BTaddress, port))
s.listen(backlog)

try:
    client, address = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            key, value = unpack('2H', data)
            print(key, value)
            #client.send()
except:
    print("Closing socket")
    client.close()
    s.close()