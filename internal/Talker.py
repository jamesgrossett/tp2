import redis
import time

HOST = '10.0.0.100' #IP address of rasberry pi
PORT = 6379 

class Talker():
    def __init__(self):
        self.r = redis.Redis(HOST, PORT)
    
    #Sends data into redis under 'label' with content of value
    def send(self, label, value):
        self.r.set(label, value)

