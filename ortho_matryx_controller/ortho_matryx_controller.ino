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


/*--------------------------------------------------*/


#include "o_m_common.h"



// This MAC Address needs to be changed!!
const char* trustedPeer = "E4:5F:01:09:37:61";

// Array for clean reading buttons
const uint32_t swPoll[MATRIX_SIZE] = {  READ_SW1, READ_SW2, READ_SW3,
                                        READ_SW4, READ_SW5, READ_SW6,
                                        READ_SW7, READ_SW8, READ_SW9  };

// Char array for TX char button data
const char* buttonReply[MATRIX_SIZE] = { 'q', 'w', 'e',
                                         'a', 's', 'd',
                                         'z', 'x', 'c' };

// BLE object
Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);


volatile uint8_t sleepCount = 0;
volatile uint8_t sleepCountLast = 0;

/*--------------------------------------------------*/




/*ISR(INT1_vect, ISR_ALIASOF(PCINT0_vect));
ISR(INT2_vect, ISR_ALIASOF(PCINT0_vect));
ISR(INT3_vect, ISR_ALIASOF(PCINT0_vect));
ISR(INT4_vect, ISR_ALIASOF(PCINT0_vect));
ISR(INT0_vect, ISR_ALIASOF(PCINT0_vect));
ISR(PCINT0_vect)
{
  // disable sleep
  sleep_disable();

  // enable peripherals
  power_all_enable();

  EIMSK = 0x00;   // Disable INT(0-3)
  EIFR  = 0x00;   // Clear any existing flags 
  adadad
  PCMSK0 = 0x00;  // Disable PCINT(6,7)
  PCIFR  = 0x00;  // Clear any existing flags
  
  TCCR1A = 0x00;
  TCCR1B = 0x00;
  TCCR1B = 0x05;  // Prescale = Fclk/1024
  TIMSK1 = 0x01;  // Timer1 overflow interrupt enable
  sleepCount = 0; // Reset sleep counter
  
  TCNT1  = 0x00;  // Reset Timer1
  TIFR1  = 0x00;  // Clear Timer1 flags

  if (!ble.begin(VERBOSE_MODE))  
    shiftOut32(err);
 
  ble.setMode(BLUEFRUIT_MODE_DATA);
  ble.println(F("Awake!"));
  ble.setMode(BLUEFRUIT_MODE_COMMAND);
}




ISR(TIMER1_OVF_vect)
{
  sleepCount++;

  ble.setMode(BLUEFRUIT_MODE_DATA);
  ble.print(F("Sleep Count = "));
  ble.println(sleepCount);
  ble.setMode(BLUEFRUIT_MODE_COMMAND);
}




void sleeping()
{ 
  ble.setMode(BLUEFRUIT_MODE_DATA);
  ble.println(F("Going to Sleep!"));
  ble.setMode(BLUEFRUIT_MODE_COMMAND);
  
  ble.flush();
  ble.end();
  DELAY_CYCLES(FCLK);

  ADCSRA = 0;
  power_all_disable ();
  
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();

  noInterrupts();

  EIMSK  = 0x0F;  // Enable INT(0-3)
  EIFR   = 0x00;  // Clear any existing flags 
      
  PCMSK0 = 0xC0;  // Enable PCINT(6,7)
  PCIFR  = 0x00;  // Clear any existing flags

  
  interrupts ();
  sleep_cpu ();
}*/




void setup() 
{
  PORTB &= ~(SW7 | SW9);
  DDRB  &= ~(SW7 | SW9);

  PORTD &= ~(SW1 | SW3 | SW4 | SW6);
  DDRD  &= ~(SW1 | SW3 | SW4 | SW6);

  PORTF &= ~(SW2 | SW5 | SW8 | DAT | CLK | LAT);
  DDRF  &= ~(SW2 | SW5 | SW8);
  DDRF  |= (DAT | CLK | LAT);

  Serial.begin(115200);
  Serial.println(F("ORTHO-MATRYX GAME DEBUG"));
  Serial.println(F("-------------------------"));
  
  DELAY_CYCLES(FCLK*2);
  shiftOut32(0);
  
  if (!ble.begin(VERBOSE_MODE))  
    shiftOut32(err); 
  
  /*if (FACTORYRESET_ENABLE) 
  {
    if (!ble.factoryReset())
      shiftOut32(err); 
  }*/

  if (!ble.sendCommandCheckOK(F("AT+GAPDEVNAME=Ortho-Matryx Controller" ))) 
    shiftOut32(err);
  

  /*if ( !ble.sendCommandCheckOK(F( "AT+BleHIDEn=On" )) )
    shiftOut32(err);*/
    

  if (!ble.sendCommandCheckOK(F("AT+BleKeyboardEn=On"))) 
    shiftOut32(err);
  
  
  ble.reset();
  ble.echo(false);
  ble.info();

  // ble callback function init
  ble.setConnectCallback(connecting);
  ble.setDisconnectCallback(disconnecting);
  ble.setBleUartRxCallback(BleUartRX);
}




void loop() 
{
  //if(sleepCount == 4)
    //sleeping();
  
  // Poll ble connect and RX data
  ble.update(200);

  // Poll and TX button data
  for(uint8_t i = 0; i < MATRIX_SIZE; i++) 
  {
      if(swPoll[i] & ((uint32_t)PINB | ((uint32_t)PIND << D_OFFSET) | ((uint32_t)PINF << F_OFFSET)))
      {
        //noInterrupts(); 
        while(swPoll[i] & ((uint32_t)PINB | ((uint32_t)PIND << D_OFFSET) | ((uint32_t)PINF << F_OFFSET))); 
        //sleepCount = 0; // Reset sleep counter
        //TCNT1  = 0;     // Reset Timer1
        //TIFR1  = 0x00;  // Clear Timer1 flags
        ble.print("AT+BleKeyboard=");
        ble.println(char(buttonReply[i]));
        Serial.print(F("keypress = "));
        Serial.println(char(buttonReply[i]));
        //interrupts ();        
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
  Serial.println(data);
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
  Serial.println(F("Connected"));
  Serial.println(peer);

  // Disconnect if peer unknown
  //if(strcmp(peer, trustedPeer) == 1) 
    //ble.disconnect(); 

  return;
}




/*--------------------------------------------
  
  Callback: BLE Disconnect
    
  > Restart sleep timer
  
--------------------------------------------*/
void disconnecting(void) 
{
  // add sleep reset
  Serial.println(F("Disconnected"));
}
