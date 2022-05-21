from BTListener import BluetoothListener
BT = BluetoothListener()
while (1):
    print(BT.recieve_keyvalue())