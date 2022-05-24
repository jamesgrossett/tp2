import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Number of steps per rotation
stepper_count = 8192

#Rotation output sequence
stepper_sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

#Delay between steps in seconds
step_delay = 0.001

class StepperMotor():
    def __init__(self, id, pins):
        self.pins = pins
        self.id = id
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)       
    
    #Rotates stepper exactly one rotation
    def rotate(self):
        step_counter = 0
        while(step_counter <= stepper_count):
            for step in stepper_sequence:
                for i in range(len(self.pins)):
                    #print(Step1Counter)
                    GPIO.output(self.pins[i], step[i])
                    sleep(step_delay)
                    step_counter+=1