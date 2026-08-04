import asyncio
from bleak import BleakScanner

async def main():
    print("Scanning for BLE devices (20 seconds)...\n")

    devices = await BleakScanner.discover(timeout=20, return_adv=True)

    if not devices:
        print("No BLE devices found.")
        return

    for address, (device, adv) in devices.items():
        print("=" * 60)
        print(f"Address : {address}")
        print(f"Name    : {device.name or 'Unknown'}")
        print(f"RSSI    : {adv.rssi}")
        print(f"Services: {adv.service_uuids}")

asyncio.run(main())
