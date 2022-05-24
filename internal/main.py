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

    #Initialise key value pair to be 0 (invalid)
    key = 0
    value = 0

    while True:
        #Things done in every state go here
        #Reset key value for each loop
        key = 0
        #Checks for incoming inventory values - indicated by key 3
        try:
            key, value = BTtalker.recieve_keyvalue()
        except Exception as e:
            print('Failed to recieve incoming key-value pair: ' + str(e))
        
        if (key == 3):
            inventory = value
        else:
            pass

        # Send new inventory value to telemetry device over both udp and bluetooth
        BTtalker.send_keyvalue(1, inventory)
        UDPtalker.send_keyvalue(1, inventory)
        
        #Waiting for user to place their hand with remaining inventory
        if state == 'waiting' and inventory > 0:
            #Display inventory value
            gpio.update_seven_seg(inventory)

            #Clear all LEDs
            gpio.clear_leds()
            
            #Close trapdoor
            gpio.write_servo(-1)
            
            #Check if hand present
            if (gpio.read_ir('hand')):
                state = 'dispensing'
        
        #Dispensing mask
        elif state == 'dispensing':
            #Turn on dispensing led 
            gpio.update_led('dispensing', 1)

            #Clear seven seg due to no looping
            gpio.clear_seven_seg()

            #Open trapdoor
            gpio.write_servo(0)

            #Rotate coil stepper one rotation
            gpio.rotate_stepper('coil')
            time.sleep(1)

            #Rotate roller stepper one rotation
            gpio.rotate_stepper('roller')

            #CHECK FOR ERROR DISPENSING HERE

            #Adjust inventory and return to waiting
            inventory-=1
            state = 'waiting'
        
        #No inventory to dispense
        elif state == 'waiting' and inventory == 0:
            #Display 0 on seven seg and enable empty led
            gpio.update_seven_seg(inventory)
            gpio.update_led('empty', 1)
        
        #Error dispensing mask detected
        elif state == 'error':
            gpio.update_led('error', 1)

            #Initialise key to be invalid (0)
            key = 0

            #Checks for incoming clear error status - indicated by key 4
            try:
                key, value = BTtalker.recieve_keyvalue()
            except Exception as e:
                print('Failed to recieve incoming key-value pair: ' + str(e))

            #If incoming message to clear error status, move to waiting
            if (key == 4 and value == 1):
                state = 'waiting'
            else:
                pass


