import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class LED():
    def __init__(self, id, pin):
        self.id = id
        self.pin = pin

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)

    def write_led(self, value):
        GPIO.output(self.pin, value)
