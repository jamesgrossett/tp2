import RPi.GPIO as GPIO
from gpiozero import Servo
from SevenSegment import SevenSegment
from LED import LED
from StepperMotor import StepperMotor
from IRSensor import IRSensor
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO ports for the 7seg pins - abcdefg header order is d1d2 bafgedc
segments =  (5,6,19,13,26,16,20)
digits = (8,7)

#GPIO ports for IR sensor input
hand_irpin = 10
error_irpin = 9

#GPIO ports for LED outputs
errorpin = 22
dispensingpin = 23
emptypin = 24

#GPIO ports for coil stepper motor driver in form (IN1, IN2, IN3, IN4)
stepper1_pins = [2, 3, 4, 14]

#GPIO ports for coil roller motor driver in form (IN1, IN2, IN3, IN4)
stepper2_pins = [15, 18, 17, 27]

#GPIO port for servo signal
servopin = 12

#Servo correction factors
myCorrection=0.45
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000

class GPIOHandler():
    def __init__(self):
        #Initialise seven segment display
        self.seven_seg = SevenSegment(segments, digits)

        #Initialise IR sensors
        self.hand_sensor = IRSensor('hand', hand_irpin)
        self.error_sensor = IRSensor('error', error_irpin)

        self.IRsensors = (self.hand_sensor, self.error_sensor)
        
        #Initialise LEDs
        self.errorled = LED('error', errorpin)
        self.dispensingled = LED('dispensing', dispensingpin)
        self.emptyled = LED('empty', dispensingpin)

        self.LEDs = (self.errorled, self.dispensingled, self.emptyled)

        #Initialise stepper motors
        self.coil_stepper = StepperMotor('coil', stepper1_pins)
        self.roller_stepper = StepperMotor('roller', stepper2_pins)

        self.stepper_motors = (self.coil_stepper, self.roller_stepper)

        #Initialise servo with gpiozero library
        self.trapdoor_servo = Servo(servopin, min_pulse_width=minPW, max_pulse_width=maxPW)
    
    #Write value to seven segment display
    def write_seven_seg(self, value):
        self.seven_seg.update_seven_seg(value)
    
    #Clear (blank) seven segment screen
    def clear_seven_seg(self):
        self.seven_seg.clear_seven_seg()

    #Reads value currently output by selected ir sensor
    def read_ir(self, id):
        for sensor in self.IRsensors:
            if sensor.id == id:
                return sensor.read_sensor()
    
    #Updates provided led in display to provided value
    def update_led(self, id, value):
        for led in self.LEDs:
            if led.id == id:
                led.write_led(value)
    
    #Sets all LEDs to off
    def clear_leds(self):
        for led in self.LEDs:
            led.write_led(0)

    #Rotate selected stepper one rotation
    def rotate_stepper(self, id):
        for stepper in self.stepper_motors:
            if stepper.id == id:
                stepper.rotate()

    #Drive trapdoor servo with a value from -1 to 1.
    def write_servo(self, value):
        i = 0
        while (i < 2000):
            self.trapdoor_servo.value = value
            i+=1

    
