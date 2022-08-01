""" -------------------------------------------------- 
    
    Ortho-Matryx BLE Communication : Pi -> Bluefruit
    Author: Ellis Hobby
   
------------------------------------------------------
    
    Help/Sources:
    
    > Web:
      https://cxiao.net/posts/2015-12-13-gatttool/
      https://dzone.com/articles/using-python-gatttool-and-bluetooth-low-energy-wit
     
    > Books via O'reilly eBooks:
      Getting Started with Bluetooth Low Energy
      Bluetooth Low Energy: The Developer's Handbook
    
------------------------------------------------------

    Info:
    
    > Spawn child process for BLE control via gatttool
    
    > Dispatch gatt process depending on argv[1]
    
    > Write input data to text file
        - Button Data  --> button.txt
        - Battry Volt  --> battery.txt
        - Random Numb  --> random.txt
        
------------------------------------------------------ 
    
    GATT Processes:
    
    > Send RGB data:
        - argv[1] = 'L' , argv[2] = '<data>'
        
    > Read button input
        - argv[1] = 'B'
    
    > Get battery value
        - argv[1] = 'V'
        
    > Get true random number
        - argv[1] = 'R'

------------------------------------------------------

    Service / Characteristic Handles:
    
    > Primary Service: Nordic UART
        UUID = 6e400001-b5a3-f393-e0a9-e50e24dcca9e
            attr handle = 0x001f
            end handle  = 0xffff
    
    > Client Characteristic Configuration Descriptor:
        UUID = 00002902-0000-1000-8000-00805f9b34fb
            handle = 0x0023
    
    > UART RX:
        UUID = 6e400003-b5a3-f393-e0a9-e50e24dcca9e
            handle = 0x0021
    
    > UART TX:
        UUID = 6e400002-b5a3-f393-e0a9-e50e24dcca9e
            handle = 0x0025

------------------------------------------------------

    Dependencies:
    
    > pexpect library
    > bluez installed  
        - gatttool in path --> ( /usr/bin/ < location > )

----------------------------------------------------- """

import sys
import pexpect

# argv[1] selects dispatch
dispatch = sys.argv[1]

# argv[2]:
# RGB output string
# Number of button reads
# Set 0 for 'V' or 'R'
data = sys.argv[2]

# Controller MAC Address
DEVICE = "D4:4A:74:16:33:BB"

# spawn new gatttool process
gatt = pexpect.spawn("gatttool -b " + DEVICE + " -I -t random")

# wait for connection
gatt.sendline("connect")
gatt.expect("Connection successful")




# helper functions
def bytesToStr (val):
    return (bytes.fromhex((val.decode()))).decode()

def strToAscii (val):
    return ((val).encode('utf-8')).hex()




# TX RGB LED data
if (dispatch == 'L'):
    
    # Convert Python string to ascii hex 
    tx = strToAscii(dispatch + data)
    
    # Tell MCU to send true random number
    gatt.sendline("char-write-cmd 0x0025 " + tx)
    
    
# Button, Battery, Random
# Notifications must be on [CCCD: 0x0023 = 0100]  
elif((dispatch =='B') or (dispatch =='V') or (dispatch =='R')):
    
    # CCCD must be set to 0100 to receive 
    gatt.sendline("char-write-cmd 0x0023 0100")

    # Dispatch: Read Buttons
    if (dispatch == 'B'):
        
        data = int(data)
        
        # Array for button inputs
        button = [0] * data
        
        # file for button data
        file = open('button.txt', 'w')
    
        # Loop to recieve X amount of inputs
        for i in range(data):
        
            # Get button input, store to array
            gatt.expect("Notification handle = 0x0021 value: ")
            gatt.expect(" \r\n")
            button[i] = bytesToStr(gatt.before)
            
            # Write input to file
            file.write(button[i])
            if(i < (data-1)):
                file.write("\n")            

    # Dispatch: Get Battery Voltage or Random Number      
    elif ((dispatch == 'V') or (dispatch == 'R')):
    
        # Convert Python string to ascii hex 
        tx = strToAscii(dispatch)
    
        # Tell MCU to send Battery Voltage
        gatt.sendline("char-write-cmd 0x0025 " + tx)

        # Wait for reply
        gatt.expect("Notification handle = 0x0021 value: ")
        gatt.expect("0a 4f 4b 0a \r\n")
        rx = bytesToStr(gatt.before)
        
        # Save data to file accordingly
        if (dispatch == 'V'):
            file = open('battery.txt', 'w')
            file.write(str(float(rx)/1000))
        
        else:
            file = open('random.txt', 'w')
            file.write(str(int(rx, 16)))
    
    else:
        print("Dispatch ERROR!!") # Add error handling?  

else:
    print("Dispatch ERROR!!") # Ditto

gatt.sendline("disconnect")


