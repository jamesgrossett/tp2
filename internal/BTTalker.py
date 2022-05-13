import socket

BTaddress = ''
port = 3


s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((BTaddress, port))

while 1:
    text = "WORKING"
    s.send(text, 'UTF-8')

#s.close

