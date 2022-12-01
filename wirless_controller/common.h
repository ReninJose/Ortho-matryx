#ifndef _COMMON_H
#define _COMMON_H

#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/interrupt.h>
#include <Arduino.h>
#include <SPI.h>
#include "Adafruit_BluefruitLE_SPI.h"

// button pin map
#define SW1  (1 << PC7)    // Port D0 , INT0
#define SW2  (1 << PD6)    // Port F7
#define SW3  (1 << PB7)    // Port D1 , INT1
#define SW4  (1 << PB6)    // Port D2 , INT2
#define SW5  (1 << PB5)    // Port F6
#define SW6  (1 << PD7)    // Port D3 , INT3
#define SW7  (1 << PC6)    // Port B6 , PCINT6
#define SW8  (1 << PD0)    // Port F5
#define SW9  (1 << PD1)    // Port B7 , PCINT7

// Offsets will be used
// to help read inputs
// within a loop
#define B_OFFSET 0
#define C_OFFSET 8
#define D_OFFSET 16

// helpers for polling
#define READ_SW1 ((uint32_t)SW1 << C_OFFSET)
#define READ_SW2 ((uint32_t)SW2 << D_OFFSET)
#define READ_SW3 ((uint32_t)SW3 << B_OFFSET)
#define READ_SW4 ((uint32_t)SW4 << B_OFFSET)
#define READ_SW5 ((uint32_t)SW5 << B_OFFSET)
#define READ_SW6 ((uint32_t)SW6 << D_OFFSET)
#define READ_SW7 ((uint32_t)SW7 << C_OFFSET)
#define READ_SW8 ((uint32_t)SW8 << D_OFFSET)
#define READ_SW9 ((uint32_t)SW9 << D_OFFSET)

// matrix size def
#define MATRIX_SIZE 9




// shift reg pin map
#define DAT (1 << PF4)
#define CLK (1 << PF1)
#define LAT (1 << PF0)

// RGB binary defs
#define RED   0x01
#define GRN   0x02
#define BLU   0x04
#define WHT   0x07



// pins for boost and regulator enable
// shutdown on sleep
#define MAX_SHDN  (1 << PF7)
#define MAX_GND_SHDN  (1 << PF6)
#define MUX_SEL   (1 << PF5)
#define BLE_SHDN  (1 << PB4)




// ERROR PATTERN: displays 'X' in RED
const uint32_t err = 0x51041041;


// BLE SPI pin map
#define BLUEFRUIT_SPI_CS    8
#define BLUEFRUIT_SPI_IRQ   7
#define BLUEFRUIT_SPI_RST   4    // Optional but recommended, set to -1 if unused

// BLE defs
#define BUFSIZE                     128   // Size of the read buffer for incoming data
#define VOLT_BUF_SIZE
#define VERBOSE_MODE                true  // If set to 'true' enables debug output
#define FACTORYRESET_ENABLE         1
#define MINIMUM_FIRMWARE_VERSION    "0.7.0"
#define MODE_LED_BEHAVIOUR          "DISABLE"
#define BAUDRATE                    "250000"

// mac address size: xx:xx:xx:xx:xx:xx
#define PEER_ADDR_SIZE  18



// avr delay helper
#define DELAY_CYCLES(n) __builtin_avr_delay_cycles(n)
#define FCLK 8000000




// sleep time and counters
#define SIX_MIN_COUNT 45







void connecting(void);
void disconnecting(void);
void BleUartRX(char data[], uint16_t len);

void outputRGB(char *rgb);
void txBattery(Adafruit_BluefruitLE_SPI& _ble);
void txRandom(Adafruit_BluefruitLE_SPI& _ble);

void prepData32(char val, uint32_t &buf);
void shiftOut32(uint32_t data);

#endif
