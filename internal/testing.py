from GPIOhandler import GPIOHandler
import time
gpio = GPIOHandler()
gpio.rotate_stepper1()
gpio.clear_leds()
gpio.clear_seven_seg()
    