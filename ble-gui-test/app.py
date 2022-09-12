import tkinter as tk
import asyncio
import gui as g
from colors import ColorDict as color
from orthoble import OrthoMatryxBLE

TITLE = 0
MENU = 1
AVATAR = 2

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.dev = OrthoMatryxBLE()
        self.state = TITLE
        
        self.dispatch = {
            0: self.title_event,
            1: self.menu_event,
            2: self.avatar_event
        }
        self.menu_transition = {
            **dict.fromkeys(['q','a','z'], self.menu_to_avatar)
            #**dict.fromkeys(['e','d','c'], self.menu_to_game)
        }
        self.avatar_transition = {
            #**dict.fromkeys(['q', 'w', 'e', 'a', 's', 'd'], self.avatar_selection)
            **dict.fromkeys(['z'], self.avatar_to_menu)
            #**dict.fromkeys(['c'], self.avatar_to_game)
        }
        self.gui = self.gui_init()
        self.set_event_bind()
        
        self.loop = asyncio.get_event_loop()       
        task = self.loop.create_task(self.run())
        try:
            self.loop.run_until_complete(task)
        except Exception as err:
            print(err)
    

    def gui_init(self):
        self.title("Ortho-Matryx Game")
        dims = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%sx%s" % (dims))
        frame = tk.Frame(self, bg='black')
        frame.pack(fill=tk.BOTH, expand=tk.YES)
        frame.update()
        return g.GUI(frame)

    def set_event_bind(self):
        buttons = [
            '<q>', '<w>', '<e>',
            '<a>', '<s>', '<d>',
            '<z>', '<x>', '<c>'
        ]
        for key in buttons:
            self.bind(key, lambda event: asyncio.ensure_future(self.state_machine(event)))


    
    async def run(self):
        self.loop.create_task(self.gui.updater())
        await self.gui.title()
        print('Entering Loop')
        while True:
            print('Looping')
            scan = await self.dev.scan()
            print('scan = %s' % (scan))
            if scan:
                print('Attempting Connection')
                await self.dev.connect()
                while self.dev.status():
                    print(self.dev.status())
                    await asyncio.sleep(5)
            else:
                self.state = TITLE
                await self.gui.title()



    async def state_machine(self, event):
        key = event.keysym
        await self.dispatch[self.state](key)

    async def title_event(self, key):
        self.state = MENU
        await self.dev.tx_rgb(color['menu'])
        await self.gui.menu()
        
        
    async def menu_event(self, key):
        if key in self.menu_transition:
            await self.menu_transition[key]()
       
    async def menu_to_avatar(self):
        self.state = AVATAR
        await self.dev.tx_rgb(color['avatar'])
        await self.gui.avatar()


    async def avatar_event(self, key):
        if key in self.avatar_transition:
            await self.avatar_transition[key]()
    
    async def avatar_to_menu(self):
        self.state = MENU
        await self.dev.tx_rgb(color['menu'])
        await self.gui.menu()

            
a = App()       