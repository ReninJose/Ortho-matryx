import bleak_test
import asyncio


async def main(client):
    await ble._disconnection()
    print("Start")
    status = await client.scanner()
    #print(status)
    
    status = await client.tx_rgb('RRRGGGBBB')
    print(status)

ble = bleak_test.PiClient()

print(ble)
asyncio.run(main(ble))