import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class IRSensor():
    def __init__(self, id, pin):
        self.id = id
        self.pin = pin

        GPIO.setup(self.pin, GPIO.IN)
    
    def read_sensor(self):
        return GPIO.input(self.pin)