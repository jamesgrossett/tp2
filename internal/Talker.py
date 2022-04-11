from itertools import filterfalse
import redis
import time

HOST = '10.0.0.100' #IP address of rasberry pi
PORT = 6379 

class Talker():
    def __init__(self):
        self.r = redis.Redis(HOST, PORT)
        self.r.set('inventory', 66)
        self.r.set('error', True)
    
    #Sends data into redis under 'label' with content of value
    def send(self, label, value):
        self.r.set(label, value)

