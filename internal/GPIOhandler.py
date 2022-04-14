import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

# GPIO ports for the 7seg pins - abcdefg
segments =  (5,6,19,13,26,16,20)
digits = (8,7)
#sevens eg delay in seconds
ssdelay = 1/120

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
        

        