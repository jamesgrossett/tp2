import socket

BTaddress = '0C:96:E6:B5:0F:BC' #Laptop bluetooth MAC address
port = 3


s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((BTaddress, port))

while 1:
    text = "WORKING"
    s.send(text, 'UTF-8')

#s.close

