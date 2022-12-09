import asyncio as io
import subprocess
from bleak import BleakClient, BleakScanner

# constants 
UART_SERVICE = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
LOCAL_NAME = 'Ortho-Matryx Controller'


class BLE:
    
    def __init__(self, controller, loop, connection_data):
       
        # save ref controller (app.py) and async loop
        self.ctrl = controller
        self.loop = loop
        
        # refs for connection
        self.connect_tx = connection_data
        self.ble_mac_address = None
        self.client = None
        self.rx = None
        
        # flags for ble synchronization
        self.scan_flag = io.Event()
        self.connected_flag = io.Event()
        
        # add scanning process to async loop
        self.loop.create_task(self.scan())
           
    
    async def scan(self):
        '''
            continuously scan while scan_flag is NOT SET
        '''
        try:
            async with BleakScanner(detection_callback=self._connect) as scan:
                await self.scan_flag.wait()
        except:
            # check if connected_flag has been set
            if not self.connected_flag.is_set():
                self.connected_flag.set()
                self.connected_flag.clear()
            
            # check if scan_flag has been set
            if not self.scan_flag.is_set():
                self.scan_flag.set()
            
            # restart scanning process
            self.scan_flag.clear()
            self.loop.create_task(self.scan())
            
            
            
    async def _connect(self, device, adv_data):
        '''
            check scanned adv data against local name
        '''
        if adv_data.local_name == LOCAL_NAME:
            
            # clear set flag, save mac address
            self.scan_flag.set()
            self.ble_mac_address = device.address
            
            # give the client a moment to initialize
            await io.sleep(2)
            
            # attempt connection
            try:
                async with BleakClient(device, disconnected_callback=self._disconnect) as client:
                    
                    # save ref to client
                    self.client = client
                    
                    # attempt to init notifications, save RX char
                    try:
                        await client.start_notify(UART_TX_UUID, self._data_recieved)
                        serv = client.services.get_service(UART_SERVICE)
                        self.rx = serv.get_characteristic(UART_RX_UUID)
                    except:
                        pass
                    
                    # send connection data (i.e. color string for menu screen)
                    await self.send_data(self.connect_tx)
                    
                    # set and clear gui idle screen flag, will propmpt menu screen
                    self.ctrl.idle_flag.set()
                    self.ctrl.idle_flag.clear()
                    
                    # maintain connection until connected_flag is set
                    await self.connected_flag.wait()
            
            # if connection fails, restart scan process
            except:
                self.scan_flag.clear()
                self.loop.create_task(self.scan())
                
                        
    def _data_recieved(self, char, data):
        '''
            decode notification data
            send to controller (app.py)
            serves as button inputs
        '''
        data = data.decode()
        self.ctrl.model_event(data)
                  
                
    def _disconnect(self, device):
        '''
            disconnect callback
            cleanup procedure for BLE
        '''
        # if GUI still in active state
        # reset flag, returns to tile screen
        if not self.ctrl.active_flag.is_set():
            self.ctrl.active_flag.set()
            self.ctrl.active_flag.clear()
        
        # remove mac address from bluez, helps with cache issues
        print(self.ble_mac_address)
        subprocess.call(['bluetoothctl', 'remove', self.ble_mac_address])
        
        # disconnect async task, helps with synchonization
        self.loop.create_task(self._disconnect_async())


    async def _disconnect_async(self):
        '''
            disconnect callback async
            cleanup procedure for BLE
        '''
        # check if connected_flag has been set
        if not self.connected_flag.is_set():
            self.connected_flag.set()
            self.connected_flag.clear()
        
        # check if scan_flag has been set
        if not self.scan_flag.is_set():
            self.scan_flag.set()
        
        # restart scanning process
        self.scan_flag.clear()
        self.loop.create_task(self.scan())
                
                
    async def disconnect(self, *args, **kwargs):
        '''
            manual disconnect
        '''
        # if GUI still in active state
        # reset flag, returns to tile screen
        if not self.ctrl.active_flag.is_set():
            self.ctrl.active_flag.set()
            self.ctrl.active_flag.clear()
        
        # if clent exists attempt to disconnect
        if self.client:
            await self.client.disconnect()
        
        
    async def send_data(self, data):
        '''
            send data to client
            input: str
        '''
        # make sure client and rx char exist
        if self.client and self.rx:
            try:
                # decode encode data
                data = ('L' + data).encode('UTF-8')
                await self.client.write_gatt_char(self.rx, data)
            except Exception:
                pass
            
