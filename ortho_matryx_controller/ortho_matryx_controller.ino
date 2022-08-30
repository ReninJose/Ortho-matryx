/*---------------------------------------------------- 
  
  Ortho-Matryx Controller
  Author: Ellis Hobby

------------------------------------------------------    

  Help/Sources:
  
  > Web:
    https://github.com/adafruit/Adafruit_BluefruitLE_nRF51
    https://learn.adafruit.com/adafruit-feather-32u4-bluefruit-le/overview

  > Books via O'reilly eBooks
    Getting Started with Bluetooth Low Energy
    Bluetooth Low Energy: The Developer's Handbook
  
------------------------------------------------------    

  Info:

  > Communicate with Raspberry Pi via BLE
  > Recieve(RX) 9 RGB LED values as strings
    - e.g. "RRRGGGBBB"
  > Transmit(TX): 
    - Buttons Press 
    - Battery Voltage 
    - Random Number
  > Output 3x3 RGB LED Matrix 
  > Enters deep sleep after timeout [? min]
  > Awake on interrupt - button press

 ------------------------------------------------------    

  Functions List:

  > void outputRGB(char *rgb);
  > void txBattery(Adafruit_BluefruitLE_SPI& _ble);
  > void txRandom(Adafruit_BluefruitLE_SPI& _ble);
  > void prepData32(char val, uint32_t &buf);
  > void shiftOut32(uint32_t data);

------------------------------------------------------    

  Callback Function List: 

  > void connecting(void);
  > void disconnecting(void);
  > void BleUartRX(char data[], uint16_t len);

------------------------------------------------------

  * TO DO :

  > Button interrputs
  > Deep sleep state
  > Sleep timer
  > 3.3V Reg and 5V Boost Shutdown

------------------------------------------------------

  * IMPORTANT NOTES:

  > Must set Pi MAC Address --> trusterPeer

------------------------------------------------------

  Dependencies:

  > Adafruit Boards Library
  > Adafruit nRF51 Library

----------------------------------------------------*/

#include "o_m_common.h"


// This MAC Address needs to be changed!!
const char* trustedPeer = "E4:5F:01:09:37:61";

// Array for clean reading buttons
const uint8_t button[MATRIX_SIZE] = {SW0, SW1, SW2, SW3, SW4, SW5, SW6, SW7, SW8};

// Char array for TX char button data
const char* replyButton[MATRIX_SIZE] = { "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"};

// BLE object
Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

void setup() 
{
  uint8_t i;
  uint8_t shiftHw[3] = {DAT, CLK, LAT};

  // set button pins input
  for(i = 0; i < 9; i++) 
    pinMode(button[i], INPUT);
  
  // set shift reg pins output
  for(i = 0; i < 3; i++) 
    pinMode(shiftHw[i], OUTPUT);

  /*Serial.begin(115200);
  Serial.println(F("ORTHO-MATRYX GAME DEBUG"));
  Serial.println(F("-------------------------"));*/
  
  delay(2000);
  shiftOut32(0);
  
  if (!ble.begin(VERBOSE_MODE))  
    shiftOut32(err); 
  
  if (FACTORYRESET_ENABLE) 
  {
    if (ble.factoryReset() ==0 )
      shiftOut32(err); 
  }
  
  ble.reset();
  ble.echo(false);

  // ble callback function init
  ble.setConnectCallback(connecting);
  ble.setDisconnectCallback(disconnecting);
  ble.setBleUartRxCallback(BleUartRX);

}

void loop() 
{
  // Poll ble connect and RX data
  ble.update(200);

  // Poll and TX button data
  for(uint8_t i = 0; i < MATRIX_SIZE; i++) 
  {
      if(digitalRead(button[i])) 
      {  
        while(digitalRead(button[i])); 
        ble.setMode(BLUEFRUIT_MODE_DATA);
        ble.print(replyButton[i]);
        ble.setMode(BLUEFRUIT_MODE_COMMAND);       
    }
  }
}



/*--------------------------------------------
  
  Callback: UART RX
    
  in:
    > data[]  - recieved data buffer
    > len     - buffer length
  
  out: 
    > check first data member
    > dispatch accordingly
    
  Dispatch Functions:
    > RGB matrix output
    > TX battery voltage
    > TX random number
    > Error pattern display

--------------------------------------------*/
void BleUartRX(char data[], uint16_t len) 
{
  switch(data[0]) 
  {
    // LED DISPATCH
    case 'L':
      outputRGB(&data[1]);
      break;
    
    // BATTERY VOLTAGE DISPATCH  
    case 'V':
      txBattery(ble);
      break;
    
    // RANDOM NUMBER DISPATCH
    case 'R':
      txRandom(ble);
      break;
    
    // INVALID DISPATCH
    default:
      shiftOut32(err);
      break;
  }
}



/*--------------------------------------------
  
  Callback: BLE Connection Attempt
    
  > check peer address
    *** Must set trustedPeer ***
  
  > connect if known
    
  > disconnect if unknown
  
--------------------------------------------*/
void connecting(void) 
{
  
  char peer[PEER_ADDR_SIZE];
 
  ble.atcommandStrReply(F("AT+BLEGETPEERADDR"), peer, (PEER_ADDR_SIZE-1), 500);

  // Disconnect if peer unknown
  if(strcmp(peer, trustedPeer) == 1) 
    ble.disconnect(); 

  return;
}



/*--------------------------------------------
  
  Callback: BLE Disconnect
    
  > Restart sleep timer
  
--------------------------------------------*/
void disconnecting(void) 
{
  // add sleep reset
}
