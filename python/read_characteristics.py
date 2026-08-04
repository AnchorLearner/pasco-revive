import asyncio
from bleak import BleakClient

ADDRESS = "80:6F:B0:A4:B9:A3"

async def main():
    async with BleakClient(ADDRESS) as client:
        print(f"Connected: {client.is_connected}\n")

        for service in client.services:
            print(f"Service: {service.uuid}")

            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)

                        print(f"  {char.uuid}")
                        print(f"    Length : {len(value)}")
                        print(f"    Hex    : {value.hex()}")
                        try:
                            print(f"    ASCII  : {value.decode('utf-8')}")
                        except UnicodeDecodeError:
                            print("    ASCII  : <binary>")
                    except Exception as e:
                        print(f"  {char.uuid}")
                        print(f"    Error: {e}")

            print()
            
asyncio.run(main())
