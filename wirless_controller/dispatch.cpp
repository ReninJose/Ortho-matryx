#include "common.h"

/*--------------------------------------------
  
  Function: Output RGB LEDs

  in:
    > String of RGB matrix values
    
  activity:
    > Fill buffer with appropriate binary
    > Send buffer to shift reg network
  
  out: 
    > RGB Matrix LEDs

--------------------------------------------*/
void outputRGB(char *rgb) 
{  
  uint32_t buffer32;
    
  for(uint8_t i = 0; i < MATRIX_SIZE; i++) 
      prepData32(rgb[i], buffer32);

    
  shiftOut32(buffer32);
  return;
}



/*--------------------------------------------
  
  Function: Transmit Battery Voltage
    
  activity:
    > Get battery voltage
  
  out: 
    > TX voltage to peer

--------------------------------------------*/
void txBattery(Adafruit_BluefruitLE_SPI& _ble) 
{ 
  char voltage[BUFSIZE];

  _ble.atcommandStrReply(F("AT+HWVBAT"), voltage, BUFSIZE, 500);
  
  _ble.setMode(BLUEFRUIT_MODE_DATA);
  _ble.print(voltage);
  _ble.setMode(BLUEFRUIT_MODE_COMMAND);
  return;
}




/*--------------------------------------------
  
  Function: TX Random Number
    
  activity:
    > Get random number (radio white noise)
  
  out: 
    > TX random number to peer

--------------------------------------------*/
void txRandom(Adafruit_BluefruitLE_SPI& _ble) {
  
  char rando[BUFSIZE];

  _ble.atcommandStrReply(F("AT+HWRANDOM"), rando, BUFSIZE, 500);
  
  _ble.setMode(BLUEFRUIT_MODE_DATA);
  _ble.print(rando);
  _ble.setMode(BLUEFRUIT_MODE_COMMAND);
  return;
}
