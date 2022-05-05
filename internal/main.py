from GPIOhandler import GPIOHandler
import time

if __name__ == '__main__':
    gpio = GPIOHandler()
    state = 'waiting'
    inventory = 5

    while True:
        #Things done in every state go here 
        
        #Waiting for user to place their hand
        if state == 'waiting':
            gpio.update_seven_seg(inventory)
            gpio.clear_leds()
            if (inventory == 0):
                state = 'empty'
            if (gpio.read_hand_sensor()):
                state = 'dispensing'
        
        #Dispensing mask
        elif state == 'dispensing':
            gpio.update_led('dispensing', 1)
            gpio.rotate_stepper1()
            gpio.update_led('dispensing', 0)
            inventory-=1
            state = 'waiting'
        
        #No inventory to dispense
        elif state == 'empty' and inventory == 0:
            if (gpio.read_hand_sensor):
                gpio.update_led('empty', 1)
                time.sleep(3)
                gpio.update_led('empty', 0)

                #Refresh inventory, go to waiting
                inventory+=5
                state = 'waiting'


