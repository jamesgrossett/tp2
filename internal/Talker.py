import redis
import time

HOST = '' #IP address of rasberry pi
PORT = 6379 

class Talker():
    def __init__(self):
        self.r = redis.Redis(HOST, PORT)
    
    #Sends data into redis under 'label' with content of value
    def send(self, label, value):
        self.r.set(label, value)

