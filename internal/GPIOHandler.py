import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#Set GPIO ports:
#7seg
#segment GPIO pins for (a, b, c, d, e, f, g)
segments = ()
digits = ()
#leds
#motors

#Define numbers for seven seg output
num = {'clear':(0,0,0,0,0,0,0),
'0':(1,1,1,1,1,1,0),
'1':(0,1,1,0,0,0,0),
'2':(1,1,0,1,1,0,1),
'3':(1,1,1,1,0,0,1),
'4':(0,1,1,0,0,1,1),
'5':(1,0,1,1,0,1,1),
'6':(1,0,1,1,1,1,1),
'7':(1,1,1,0,0,0,0),
'8':(1,1,1,1,1,1,1),
'9':(1,1,1,1,0,1,1)}

class GPIOHandler():
    def __init__(self):


        #setup 7seg display
        for segment in segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

        for digit in digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)
        
            
    #Displays 2-digit value on seven seg (to be implemented via loop)
    def update_7seg(self, value):
        digit1 = value//10
        digit2 = value%10
        #Display digit 1
        GPIO.output(self.digits[0], 1)
        GPIO.output(self.digits[1], 0)
        digit1_segments = num.get(str(digit1))
        for segment in digit1_segments:
            GPIO.output(segment, digit1_segments[segment])
        
        #Display digit 2
        GPIO.output(self.digits[0], 0)
        GPIO.output(self.digits[1], 1)
        digit2_segments = num.get(str(digit2))
        for segment in digit2_segments:
            GPIO.output(segment, digit2_segments[segment])
        