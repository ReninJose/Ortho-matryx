#include <Arduino.h>
#include <SPI.h>
#include "o_m_common.h"

/*--------------------------------------------
  
  Function: Prepare 32 Bit Shift Reg Value

   in:
   > RGB character value ('R', 'G', 'B')
   > 32-bit buffer address
  
  activity:
    > Shift corresponding bits into buffer

--------------------------------------------*/
void prepData32(char val, uint32_t& buf) 
{ 
  uint8_t bits;
  
  switch(val) 
  {
    case 'R':
      bits = RED;
      break;
    case 'G':
      bits = GRN;
      break;
    case 'B':
      bits = BLU;
      break;
    default:
      bits = 0;
      break;
  }
  buf = (buf << 3) | bits;
}



/*--------------------------------------------
  
  Function: RGB Shift Register Output

   in:
   > 32-bit shift data
  
  activity:
    > Shift data out to display RGB pattern

--------------------------------------------*/
void shiftOut32(uint32_t data) 
{  
  digitalWrite(LAT, LOW);
  
  for(uint8_t i = 0; i < 32; i++) 
  {
    digitalWrite(DAT, ((data >> (31-i)) & 0x00000001));
    delay(1);
    
    digitalWrite(CLK, LOW);
    delay(1);
    
    digitalWrite(CLK, HIGH);
    delay(1);
  }
  digitalWrite(LAT, HIGH);
}
