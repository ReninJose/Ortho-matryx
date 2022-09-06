import asyncio
import bleak

MAC = "D4:4A:74:16:33:BB"
TX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
RX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'


"""def rx_callback(peripheral, data):
    data = bytes(data).decode('UTF-8')
    data = data.removesuffix('\nOK\n')
    if(data[0] == '0'):
        data = int(data, 16)
    else:
        data = int(data)
    
    print(type(data))
    print(data)

async def main()
    client = bleak.BleakClient(MAC)
    try:
        await client.connect()
        await client.start_notify(RX_UUID, rx_callback)
        await asyncio.sleep(2.0)
        await client.write_gatt_char(TX_UUID, 'R'.encode('UTF-8'))
        await asyncio.sleep(2.0)
        await client.stop_notify(RX_UUID)
        
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()
        print("Disconnected!")"""
        
        
class PiClient:
    def __init__(self):
        self.client = bleak.BleakClient(MAC)
        self.client.set_disconnected_callback(self._disconnect_callback)
        self.scan = bleak.BleakScanner(self._scanner_callback)
        self.rx_buf = None
        self.rx_status = False
        self.dev_status = False
        
    def _scanner_callback(self, devs, adv_data):
        if(devs.address == MAC):
            print("Ready: _scanner_callback")
            self.dev_status = True
            print("dev_status = " + str(self.dev_status))
        else:
            self.dev_status = False
        
    async def scanner(self) -> bool:
        await self.scan.start()
        await asyncio.sleep(2.0)
        await self.scan.stop()
        return self.dev_status
    
    def _disconnect_callback(self, client):
        self.dev_status = False
        print("Disconnect Callback")
        print(self.dev_status)
    
    async def _connection(self):
        try:
            await self.client.connect()
            #self.dev_status = True
            print("Connected")
            print(self.dev_status) 
        except Exception as e:
            print(e)
        finally:
            await self.client.disconnect()
            #self.dev_status = False
            print("Disconnect")
            print(self.dev_status)
            
    async def _disconnection(self):
        await self.client.disconnect()
            
    async def _tx(self, data):
        await self.client.write_gatt_char(TX_UUID, data.encode('UTF-8'))
        
    def _rx_callback(self, peripheral, data):
        self.rx_buf = bytes(data).decode('UTF-8')
        self.rx_buf = data.removesuffix('\nOK\n')
        self.rx_status = True
              
    async def _rx(self, wait_time):
        self.rx_status = False
        await self.client.start_notify(RX_UUID, _rx_callback)
        await asyncio.sleep(wait_time)
        await self.client.stop_notify(RX_UUID)
                 
    async def tx_rgb(self, rgb) -> bool:
        await self._connection()
        if(self.dev_status):
            #await self.client.write_gatt_char(TX_UUID, rgb.encode('UTF-8'))
            await self._tx('L' + rgb)
            await self.client.disconnect()
            return True
        else:
            return False
                
    async def rx_button(self):
        self._connection()
        if(self.dev_status):
            await self._rx(wait_time=360)
            if(self.rx_status):
                print("RX Button Good")
                print("rx_buf = %s" % (self.rx_buf))
                return self.rx_buf
            else:
                print("RX Failed")
                self.rx_buf = None
                return self.rx_buf
        else:
            self.rx_buf = None
            return self.rx_buf