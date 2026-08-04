import asyncio
from bleak import BleakClient

ADDRESS = "80:6F:B0:A4:B9:A3"

async def main():
    async with BleakClient(ADDRESS) as client:
        print(f"Connected: {client.is_connected}")

        print("\nServices and Characteristics\n")

        for service in client.services:
            print(f"\nService: {service.uuid}")

            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid}")
                print(f"    Properties: {char.properties}")

asyncio.run(main())
