from GPIOhandler import GPIOHandler
import time

if __name__ == '__main__':
    gpio = GPIOHandler()
    i = 26
    while True:
        if (i > 90):
            i = 0
        gpio.clear_seven_seg()
        gpio.update_seven_seg(i)
        #i+=1
        #time.sleep(1/200)
