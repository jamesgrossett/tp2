import bluetooth
from struct import pack

BTaddress = '0c:96:e6:b5:0f:bc' #Laptop bluetooth MAC address
port = 5


s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((BTaddress, port))

while 1:
    key = 1
    value = 2
    message = pack('2H', key, value)
    s.send(message, 'UTF-8')

#s.close


