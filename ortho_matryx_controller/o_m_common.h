#ifndef _ORTHO_MATRYX_COMMON_H
#define _ORTHO_MATRYX_COMMON_H

#include <Arduino.h>
#include <SPI.h>
#include "Adafruit_BluefruitLE_SPI.h"

// button pin map
#define SW0 18
#define SW1 19
#define SW2 20
#define SW3 21
#define SW4 22
#define SW5 23
#define SW6 6
#define SW7 9
#define SW8 10

// matrix size def
#define MATRIX_SIZE 9



// shift reg pin map
#define DAT   13
#define CLK   12  
#define LAT   11

// RGB binary defs
#define RED   0x01
#define GRN   0x02
#define BLU   0x04

// ERROR PATTERN: displays 'X' in RED
const uint32_t err = 0x51041041;


// BLE SPI pin map
#define BLUEFRUIT_SPI_CS    8
#define BLUEFRUIT_SPI_IRQ   7
#define BLUEFRUIT_SPI_RST   4    // Optional but recommended, set to -1 if unused

// BLE defs
#define BUFSIZE                     128   // Size of the read buffer for incoming data
#define VERBOSE_MODE                true  // If set to 'true' enables debug output
#define FACTORYRESET_ENABLE         1
#define MINIMUM_FIRMWARE_VERSION    "0.7.0"
#define MODE_LED_BEHAVIOUR          "MODE"

// mac address size: xx:xx:xx:xx:xx:xx
#define PEER_ADDR_SIZE  18



void connecting(void);
void disconnecting(void);
void BleUartRX(char data[], uint16_t len);

void outputRGB(char *rgb);
void txBattery(Adafruit_BluefruitLE_SPI& _ble);
void txRandom(Adafruit_BluefruitLE_SPI& _ble);

void prepData32(char val, uint32_t &buf);
void shiftOut32(uint32_t data);

#endif
