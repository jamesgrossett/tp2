from GPIOHandler import GPIOHandler
from gpiozero import Servo

if __name__ == '__main__':
    gpio = GPIOHandler()
    i = 0
    #while(1):
        #gpio.write_servo(500)
    while (1):
        #servo = Servo(12)
        #servo.max()
        print(gpio.read_ir('error'))
        #i+=1

        #-1 is closed, 0 is open
    

