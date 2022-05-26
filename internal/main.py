from GPIOHandler import GPIOHandler
from UDPTalker import Talker
from BTTalker import BluetoothTalker
import time

if __name__ == '__main__':
    gpio = GPIOHandler()
    UDPtalker = Talker()
    BTtalker = BluetoothTalker()
    state = 'waiting'
    
    #Initialise and send starting inventory value
    inventory = 11
    UDPtalker.send_keyvalue(1, inventory)

    #Initialise key value pair to be 0 (invalid)
    key = 0
    value = 0

    #Close trapdoor initially
    gpio.write_servo(600)

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
            #Send cleared error status to telemetry unit
            BTtalker.send_keyvalue(2, 0)
            
            #Display inventory value
            gpio.write_seven_seg(inventory)

            #Clear all LEDs
            gpio.clear_leds()
            
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
            gpio.write_servo(1600)

            #Rotate coil stepper one rotation
            gpio.rotate_stepper('coil')
            time.sleep(0.25)

            #Attempt to dispense mask 3 times
            for attempt in range(3):
                print(f'Dispensing attempt {attempt}')
                gpio.rotate_stepper('roller')
                #Check mask is present (ie successful dispension) after rolling one rotation
                if (gpio.read_ir('error') == 1):
                    #Adjust inventory and return to waiting upon successful dispension
                    inventory-=1
                    state = 'waiting'
                    break
                else:
                    attempt+=1
                
                #If all attempts failed, indicate error
                if attempt == 3:
                    print('All attempts failed')
                    inventory-=1
                    state = 'error'
        
        #No inventory to dispense - empty
        elif state == 'waiting' and inventory == 0:
            #Display 0 on seven seg and enable empty led
            gpio.write_seven_seg(inventory)
            gpio.update_led('empty', 1)
        
        #Error dispensing mask detected
        elif state == 'error':
            gpio.update_led('error', 1)

            #Send error status to telemetry device
            BTtalker.send_keyvalue(2, 1)          

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


