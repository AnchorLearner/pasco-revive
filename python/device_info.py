import asyncio
from bleak import BleakClient

ADDRESS = "80:6F:B0:A4:B9:A3"

INFO = {
    "00002a29-0000-1000-8000-00805f9b34fb": "Manufacturer",
    "00002a24-0000-1000-8000-00805f9b34fb": "Model",
    "00002a26-0000-1000-8000-00805f9b34fb": "Firmware",
    "00002a27-0000-1000-8000-00805f9b34fb": "Hardware",
    "00002a25-0000-1000-8000-00805f9b34fb": "Serial",
}

async def main():

    async with BleakClient(ADDRESS) as client:

        for uuid, name in INFO.items():

            try:

                value = await client.read_gatt_char(uuid)

                print(name, ":", value.decode(errors="ignore"))

            except Exception as e:

                print(name, e)

asyncio.run(main())
