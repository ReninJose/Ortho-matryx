from bleak import BleakClient, BleakScanner
import asyncio
import subprocess

ADDRESS = 'D4:4A:74:16:33:BB'
TX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'

class OrthoMatryxBLE():
    def __init__(self):
        self.client = None
   
        
    def disconnected(self, client):
        print('disconnect')
        
    
    async def scan(self):
        subprocess.call(['bluetoothctl', 'remove', ADDRESS])
        device = await BleakScanner.find_device_by_address(ADDRESS, timeout=10.0)
        print('device = %s' % (device))
        if not device:
            self.client = None
            return False
        else:
            self.client = BleakClient(device)
            print(self.client)
            self.client.set_disconnected_callback(self.disconnected)
            return True
        
    async def connect(self):
        print(self.client)
        try:
            #sub = subprocess.call(['bluetoothctl', 'remove', ADDRESS])
            #print(sub)
            await self.client.connect(timeout=10.0)
            print("connected")
        except Exception as e:
            print('exception')
            print(e)
            await self.client.disconnect()
            return False
        finally:
            return self.client.is_connected
        
    async def tx_rgb(self, color_string):
        tx = ('L' + color_string).encode('UTF-8')
        print(tx)
        try:
            await self.client.write_gatt_char(TX_UUID, tx)
        except Exception as e:
            print(e)
            return False
        finally:
            return True
        
    def status(self)->bool:
        status = self.client.is_connected
        return status
    
    async def disconnect(self):
        await self.client.disconnect()