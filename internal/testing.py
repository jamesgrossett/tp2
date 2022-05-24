from GPIOhandler import GPIOHandler
from gpiozero import Servo

if __name__ == '__main__':
    gpio = GPIOHandler()
    i = 0
    while i < 2000:
        #servo = Servo(12)
        #servo.max()
        gpio.write_servo(0)
        i+=1

        #-1 is closed, 0 is open
    

