#https://github.com/ukBaz/BLE_GATT/tree/3c57ce9a0b85dc683555ee0922ebc565ca7fe24f

import BLE_GATT
from gi.repository import GLib

MAC = 'D4:4A:74:16:33:BB'
TX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
RX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
CCCD_UUID = '00002902-0000-1000-8000-00805f9b34fb'

LED_DISPATCH = 'L'
VOLT_DISPATCH = 'V'
RAND_DISPATCH = 'R'

BUTTON_TIMEOUT = 360
VOLT_TIMEOUT = 10
RAND_TIMEOUT = 10

class Controller(BLE_GATT.Central):
    def __init__(self):
        super().__init__(address=MAC)
        self.rx_buffer = None
        self.event_id = 0
        self.err_status = 0
        
    def error_status(self):
        return self.err_staus

    def tx_generic(self, uuid='', dispatch='', data=''):
        try:
            self.connect()
            self.char_write(uuid, (dispatch+data).encode('utf-8'))
            self.err_status = 0
            self.disconnect()
        except:
            print("Error")
            self.err_status = 1

    def rx_callback(self, data):
        self.rx_buffer = bytes(data).decode('UTF-8')
        print("RX Complete")
        print(data)
        print(self.rx_buffer)
        self.err_status = 0
        GLib.source_remove(self.event_id)
        self.cleanup()
        

    def timeout_callback(self):
        print("Timeout Error")
        self.err_status = 1
        self.cleanup()
        return False

    def rx_generic(self, dispatch='', timeout=0):
        try:
            self.connect()
            self.char_write(TX_UUID, (dispatch).encode('utf-8'))
            self.on_value_change(RX_UUID, self.rx_callback)
            self.event_id = GLib.timeout_add_seconds(timeout, self.timeout_callback)
            self.wait_for_notifications()
            print("Notifications off")
            
        except:
            print("Error")
            self.err_status = 1

    def tx_rgb(self, rgb):
        self.tx_generic(uuid=TX_UUID, dispatch=LED_DISPATCH, data=rgb)
        return self.err_status
         
    def rx_button(self):
        self.rx_generic(timeout=BUTTON_TIMEOUT)
        return self.err_status
        
    def rx_voltage(self):
        self.rx_generic(dispatch=VOLT_DISPATCH, timeout=VOLT_TIMEOUT)
        return self.err_status
        
    def rx_random(self):
        self.rx_generic(dispatch=RAND_DISPATCH, timeout=RAND_TIMEOUT)
        return self.err_status



"""
import sys
import pexpect
import pydbus
from gi.repository import GLib



MAC = 'D4_4A_74_16_33_BB'
TX_PATH = '/org/bluez/hci0/dev_D4_4A_74_16_33_BB/service001f/char0024'
RX_PATH = '/org/bluez/hci0/dev_D4_4A_74_16_33_BB/service001f/char0020'
CCCD_PATH = '/org/bluez/hci0/dev_D4_4A_74_16_33_BB/service001f/char0020/desc0023'
BLUEZ_SERVICE = 'org.bluez'
ADAPTER_PATH = '/org/bluez/hci0'
DEVICE_PATH = f"{ADAPTER_PATH}/dev_{MAC}"

class Controller():
    def __init__(self):
        
        self.bus = pydbus.SystemBus()
        self.adapter = self.bus.get(BLUEZ_SERVICE, ADAPTER_PATH) 
        self.device = self.bus.get(BLUEZ_SERVICE, DEVICE_PATH)
        
        print(dir(self.bus))
        print(dir(self.adapter))

        self.tx = self.bus.get(BLUEZ_SERVICE, TX_PATH)
        self.rx = self.bus.get(BLUEZ_SERVICE, RX_PATH)
        self.cccd = self.bus.get(BLUEZ_SERVICE, CCCD_PATH)
        
        print(self.tx)
        print(self.rx)
        print(self.cccd)

    def connect(self):
        try:
            self.device.Connect()
            print("Connected")
        except:
            print("Connection Error")
            return 0

    def disconnect(self):
        try:
            self.device.Disconnect()
        except:
            pass

    def tx_rgb(self, data):
        try:
            self.connect()
            self.tx.WriteValue((data.encode('utf-8')), {})
            self.disconnect()
        except:
            print("TX Error")
            return 0
        
    def rx_handler(self):
        pass
        
    

    def rx_button(self):
        mainloop = GLib.MainLoop()
        self.rx.onPropertiesChanged = self.rx_handler
        self.rx.StartNotify()
        try:
            mainloop.run()
        except KeyboardInterrupt:
            mainloop.quit()
            self.rx.StopNotify()
            self.device.Disconnect()

 """    



        


