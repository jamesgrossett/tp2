from BTTalker import BluetoothTalker
import random

bt = BluetoothTalker()
while (1):
    bt.send_keyvalue(1, random.randint(1, 99))
    bt.send_keyvalue(2, random.randint(0, 1))