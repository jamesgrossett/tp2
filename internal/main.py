from GPIOhandler import GPIOHandler
from UDPTalker import Talker
from BTTalker import BluetoothTalker
import time

if __name__ == '__main__':
    gpio = GPIOHandler()
    UDPtalker = Talker()
    BTtalker = BluetoothTalker()
    state = 'waiting'
    
    #Initialise and send inventory value
    inventory = 14
    UDPtalker.send_keyvalue(1, inventory)

    while True:
        #Things done in every state go here
        # Send new inventory value to telemetry device over both udp and bluetooth
        BTtalker.send_keyvalue(1, inventory)
        UDPtalker.send_keyvalue(1, inventory)
        
        #Waiting for user to place their hand
        if state == 'waiting':
            #Display inventory value
            gpio.update_seven_seg(inventory)

            #Clear all LEDs
            gpio.clear_leds()

            #Check if empty
            if (inventory == 0):
                state = 'empty'
            if (gpio.read_hand_sensor()):
                state = 'dispensing'
        
        #Dispensing mask
        elif state == 'dispensing':
            #Clear seven seg due to no looping
            gpio.clear_seven_seg()

            #Turn on dispensing led and rotate dispensor stepper 1 rotation
            gpio.update_led('dispensing', 1)
            gpio.rotate_stepper1()
            #CHECK FOR ERROR DISPENSING HERE

            #Adjust inventory and return to waiting
            inventory-=1
            state = 'waiting'
        
        #No inventory to dispense
        elif state == 'empty' and inventory == 0:
            #Display 0 on seven seg and enable empty led
            gpio.update_seven_seg(inventory)
            gpio.update_led('empty', 1)

        #This indicates reload has occurred and inventory has been updated from telemetry unit
        elif state == 'empty' and inventory > 0:
            state = 'waiting'
        
        #Error dispensing mask detected
        elif state == 'error':
            gpio.update_led('error', 1)
            #leave error state after intel from telemetry


