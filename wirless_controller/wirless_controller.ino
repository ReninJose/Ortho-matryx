
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
  > Enters deep sleep after timeout [6 min]
  > Awake on interrupt - button press

 ------------------------------------------------------    

  Functions List:

  > void outputRGB(char *rgb);
  > void txBattery(Adafruit_BluefruitLE_SPI& _ble);
  > void txRandom(Adafruit_BluefruitLE_SPI& _ble);
  > void prepData32(char val, uint32_t &buf);
  > void shiftOut32(uint32_t data);
  > void port_init(void)
  > void ble_init(void)
  > void interrupt_init(void)
  > void poll_input(void)
  > void enter_sleep(void)

------------------------------------------------------    

  Callback Function List: 

  > void connecting(void);
  > void disconnecting(void);
  > void BleUartRX(char data[], uint16_t len);

------------------------------------------------------

  Interrupt Function List: 

  > ISR(INT3_vect)
  > ISR(TIMER3_OVF_vect)


------------------------------------------------------

  * TO DO :

  > 

------------------------------------------------------

  * IMPORTANT NOTES:

  > Must set Pi MAC Address --> trusterPeer

------------------------------------------------------

  Dependencies:

  > Adafruit Boards Library
  > Adafruit nRF51 Library

----------------------------------------------------*/


/*--------------------------------------------------*/


#include "common.h"



// This MAC Address needs to be changed!!
const char* trustedPeer = "DC:A6:32:6D:A0:58";

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


volatile uint8_t sleep_count = 0;
volatile uint8_t last_sleep_count = 0;


/*--------------------------------------------------*/




// External Interrupt
// Awake MCU from Sleep
ISR(INT3_vect)
{
  sleep_count = 0;
  sleep_disable();

  // Enable MAX Boost Conv, Switch MUX Routing
  PORTF |= (MAX_SHDN | MAX_GND_SHDN | MUX_SEL);

  power_adc_enable(); // ADC converter
  power_spi_enable(); // SPI
  power_usart0_enable(); // Serial (USART)
  power_timer0_enable(); // Timer 0
  power_timer1_enable(); // Timer 1
  power_timer2_enable(); // Timer 2
  power_twi_enable(); // TWI (I2C)

  // Start BLE Advertisement
  ble.setMode(BLUEFRUIT_MODE_COMMAND);
  if (!ble.sendCommandCheckOK(F("AT+GAPSTARTADV"))) 
    shiftOut32(err);
  ble.setMode(BLUEFRUIT_MODE_DATA);

  // TIMER3 INT
  TCNT3 = 0x00;           // reset count
  TIFR3 |= (1 << TOV3);   // clear flags
  TIMSK3 |= (1 << TOIE3); // enable
  
  // EXT INT3
  EIMSK &= ~(1 << INT3);  // disable ext int 3
}


// Timer OVF Interrupt
ISR(TIMER3_OVF_vect)
{
  sleep_count++;
}



/*--------------------------------------------

  Function: Initiate Ports
  
  activity:
    > set button inputs
    > set peripheral outputs

--------------------------------------------*/
void port_init(void)
{
  PORTB &= ~(SW3 | SW4 | SW5);
  DDRB  &= ~(SW3 | SW4 | SW5);

  PORTC &= ~(SW1 | SW7);
  DDRC  &= ~(SW1 | SW7);

  PORTD &= ~(SW2 | SW6 | SW8 | SW9);
  DDRD  &= ~(SW2 | SW6 | SW8 | SW9);

  PORTF &= ~(DAT | CLK | LAT | MAX_SHDN | MAX_GND_SHDN | MUX_SEL);
  DDRF  |= (DAT | CLK | LAT | MAX_SHDN | MAX_GND_SHDN | MUX_SEL);
  PORTF |= (MAX_SHDN | MAX_GND_SHDN | MUX_SEL);
}



/*--------------------------------------------

  Function: Initiate BLE Radio
  
  activity:
    > set advertise name
    > check advertise on/off 
    > set callbacks
    > set main tx mode (data)

--------------------------------------------*/
void ble_init(void)
{
  

  if (!ble.begin(VERBOSE_MODE))  
    shiftOut32(err); 

  if (!ble.sendCommandCheckOK(F("AT+GAPSTOPADV"))) 
    shiftOut32(err);

  if (!ble.sendCommandCheckOK(F("AT+GAPSTARTADV"))) 
    shiftOut32(err);

  if (!ble.sendCommandCheckOK(F("AT+GAPDEVNAME=Ortho-Matryx Controller"))) 
    shiftOut32(err);
  
  ble.sendCommandCheckOK("AT+HWModeLED=" MODE_LED_BEHAVIOUR);

  ble.sendCommandCheckOK("AT+BAUDRATE=" BAUDRATE);
  
  ble.reset();
  ble.echo(false);

  // ble callback function init
  ble.setConnectCallback(connecting);
  ble.setDisconnectCallback(disconnecting);
  ble.setBleUartRxCallback(BleUartRX);

  DELAY_CYCLES(FCLK*5);

  // Set module to DATA mode
  ble.setMode(BLUEFRUIT_MODE_DATA);  
}


/*--------------------------------------------

  Function: Initiate Interrupts
  
  activity:
    > setup ext int3
    > setup timer3 int 

--------------------------------------------*/
void interrupt_init(void)
{
  // EXT INT3
  EIMSK &= ~(1 << INT3);  // disable
  EICRA |= (1 << ISC31);  // falling edge
  EIFR |= (1 << INTF3);   // clear flags

  // TIMER3 INT
  TCCR3A = 0x00;                        // clear control register A
  TCCR3B = 0x00;                        // clear control register B
  TCCR3B = (1 << CS32) | (1 << CS30);   // set prescale = 1024 => (8 MHz)/(1024) = 7.8 kHz = Tclk
  TCNT3 = 0x00;                         // reset count to 0
  TIFR1 = (1 << TOV1);                  // clear flags
  TIMSK3 = (1 << TOIE3);                // enable overflow interrupt
}




void setup() 
{
  port_init();
  
  DELAY_CYCLES(FCLK);
  shiftOut32(0);
  
  interrupt_init();
  ble_init();
}




void loop() 
{
  // Poll Connect and Data RX
  ble.update(200);
  /*
  if ( sleep_count != last_sleep_count )
  {
    ble.print(F("sleep_count = "));
    ble.println(sleep_count);
    last_sleep_count = sleep_count;
  }
  */
  
  if(sleep_count == SIX_MIN_COUNT)
    enter_sleep();
  
  // Poll and TX button data
  poll_input();
}



/*--------------------------------------------

  Function: Enter Sleep
  
  activity:
    > shut down peripherals
    > stop ble advertise
    > enable external int3
    > disable timer3 int

--------------------------------------------*/
void enter_sleep(void)
{
  // Disable MAX Boost Conv, Rout MUX to EXT INT
  PORTF &= ~(MAX_SHDN | MAX_GND_SHDN | MUX_SEL);

  ble.println(F("Going to sleep..."));

  // Disconnect BLE
  // Slight delay helps reliablity
  DELAY_CYCLES(FCLK*1);
  ble.disconnect();
  DELAY_CYCLES(FCLK*1);
  
  // Stop BLE Advertise
  ble.setMode(BLUEFRUIT_MODE_COMMAND);
  if (!ble.sendCommandCheckOK(F("AT+GAPSTOPADV"))) 
    shiftOut32(err);
  ble.setMode(BLUEFRUIT_MODE_DATA);
  DELAY_CYCLES(FCLK*2);

  // Clear LEDs  
  shiftOut32(0);  

  cli();
  
  // EXT INT3
  EIFR |= (1 << INTF3); // clear flags
  EIMSK |= (1 << INT3); // enable
  
  // TIMER3 INT
  TIMSK3 &= ~(1 << TOIE3);  // disable
  TCNT3 |= 0x00;            // reset count
  TIFR3 |= (1 << TOV3);     // clear flags

  // Disable peripherals
  // Helps decrease power 
  power_adc_disable(); 
  power_spi_disable(); 
  power_usart0_disable();
  power_timer0_disable();
  power_timer1_disable();
  power_timer2_disable();
  power_twi_disable(); 

  sei();

  // Enter Sleep
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  sleep_cpu();  
}



/*--------------------------------------------
  
  Function: Poll Button Inputs
  
  activity:
    > check state buttons
    > if press, hold until release
    > reset sleep and timer count
    > ble tx button data

--------------------------------------------*/
void poll_input(void)
{
  for(uint8_t i = 0; i < MATRIX_SIZE; i++) 
  {
    if(swPoll[i] & ((uint32_t)PINB | ((uint32_t)PINC << C_OFFSET) | ((uint32_t)PIND << D_OFFSET)))
    { 
      sleep_count = 0;
      cli();
      
      // Hold until switch released, prevents spam data
      while(swPoll[i] & ((uint32_t)PINB | ((uint32_t)PINC << C_OFFSET) | ((uint32_t)PIND << D_OFFSET))); 
      
      TCNT3  = 0x00;          // Reset Timer3
      TIFR3 |= (1 << TOV3);   // clear int flags
      sei(); 

      // BLE TX Button Pressed
      ble.print(char(buttonReply[i]));    
      //ble.print("AT+BleKeyboard=");
      //ble.println(char(buttonReply[i])); 
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
  
  ble.setMode(BLUEFRUIT_MODE_COMMAND);
  ble.atcommandStrReply(F("AT+BLEGETPEERADDR"), peer, (PEER_ADDR_SIZE-1), 500);
  ble.setMode(BLUEFRUIT_MODE_DATA);


  // Disconnect if peer unknown
  if(strcmp(peer, trustedPeer) != strcmp(peer, trustedPeer)) 
    ble.disconnect(); 

  return;
}




/*--------------------------------------------
  
  Callback: BLE Disconnect
    
  > On disconnect enter low power sleep
  
--------------------------------------------*/
void disconnecting(void) 
{
  
  enter_sleep();
}

