import RPi.GPIO as GPIO
from gpiozero import Servo
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# GPIO ports for the 7seg pins - abcdefg header order is d1d2 bafgedc
segments =  (5,6,19,13,26,16,20)
digits = (8,7)
#sevens seg delay in seconds
ssdelay = 1/120

#GPIO ports for IR sensor output
handsensor = 10
errorsensor = 9

#GPIO port for servo signal
servopin = 12

#GPIO ports for LED outputs
errorled = 22
dispensingled = 23
emptyled = 24

#GPIO ports for ULN2003 stepper motor driver - spring driver
stepper1_1 = 2 
stepper1_2 = 3
stepper1_3 = 4
stepper1_4 = 14
stepper1_pins = [stepper1_1, stepper1_2, stepper1_3, stepper1_4]

#GPIO ports for ULN2003 stepper motor driver - roller driver
stepper2_1 = 15
stepper2_2 = 18
stepper2_3 = 17
stepper2_4 = 27
stepper2_pins = [stepper2_1, stepper2_2, stepper2_3, stepper2_4]

#stepper motor parameters
stepper_count = 4096*2

stepper_sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

#Servo correction factors
myCorrection=0.45
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000

num = {'clr':[1,1,1,1,1,1,1],
    '0':[0,0,0,0,0,0,1],
    '1':[1,0,0,1,1,1,1],
    '2':[0,0,1,0,0,1,0],
    '3':[0,0,0,0,1,1,0],
    '4':[1,0,0,1,1,0,0],
    '5':[0,1,0,0,1,0,0],
    '6':[0,1,0,0,0,0,0],
    '7':[0,0,0,1,1,1,1],
    '8':[0,0,0,0,0,0,0],
    '9':[0,0,0,1,1,0,0,]}

class GPIOHandler():
    def __init__(self):
    
        #Seven segment display
        #Setup segment GPIO
        for segment in segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 1)

        #Setup digit GPIO
        for digit in digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

        #Setup IR sensors
        GPIO.setup(handsensor, GPIO.IN)

        #Setup LED outputs
        GPIO.setup(errorled, GPIO.OUT)
        GPIO.setup(dispensingled, GPIO.OUT)
        GPIO.setup(emptyled, GPIO.OUT)

        #Setup servo with gpiozero library
        self.trapdoor_servo = Servo(servopin, min_pulse_width=minPW, max_pulse_width=maxPW)

        #Setup stepper motor outputs
        for pin in stepper1_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        
        #Setup stepper motor outputs
        for pin in stepper2_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    def clear_seven_seg(self):
        GPIO.output(digits[0], 0)
        GPIO.output(digits[1], 0)

        for i in range(7):
            GPIO.output(segments[i], 1)

    def update_seven_seg(self, value):
        digit1 = value//10
        digit2 = value%10

        #digit1 first
        GPIO.output(digits[0], 1)
        GPIO.output(digits[1], 0)
        display1 = num.get(str(digit1))
        for i in range(7):
            GPIO.output(segments[i], display1[i])
        
        time.sleep(ssdelay)

        #digit2
        GPIO.output(digits[0], 0)
        GPIO.output(digits[1], 1)
        display2 = num.get(str(digit2))
        for i in range(7):
            GPIO.output(segments[i], display2[i])
        
        time.sleep(ssdelay)
    
    #Reads value currently output by hand sensor
    def read_hand_sensor(self):
        return GPIO.input(handsensor)
    
    #Updates provided led in display
    def update_led(self, id, value):
        if (id == 'error'):
            GPIO.output(errorled, value)
        elif (id == "dispensing"):
            GPIO.output(dispensingled, value)
        elif (id == 'empty'):
            GPIO.output(emptyled, value)
    
    #Sets all LEDs to off
    def clear_leds(self):
        GPIO.output(errorled, 0)
        GPIO.output(dispensingled, 0)
        GPIO.output(emptyled, 0)

    def rotate_stepper1(self):
        Step1Counter = 0
        while(Step1Counter <= stepper_count):
            for step in stepper_sequence:
                for i in range(len(stepper1_pins)):
                    #print(Step1Counter)
                    GPIO.output(stepper1_pins[i], step[i])
                    time.sleep(0.001)
                    Step1Counter+=1

    def rotate_stepper2(self):
        Step2Counter = 0
        while(Step2Counter <= stepper_count):
            #print("Rotating stepper two")
            for step in stepper_sequence:
                for i in range(len(stepper2_pins)):
                    #print(Step1Counter)
                    GPIO.output(stepper2_pins[i], step[i])
                    time.sleep(0.001)
                    Step2Counter+=1

    #Value -1 to 1
    def write_servo(self, value):
        print(f'Writing servo to {value}')
        self.trapdoor_servo.value = value