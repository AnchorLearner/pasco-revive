import time

from pasco import PASCOBLEDevice


TARGET_ID = "795-427"

MAX_SCAN_ATTEMPTS = 3
SCAN_RETRY_DELAY = 3


def connect_cart():
    """
    Scan for the PASCO Smart Cart and connect to it.

    Returns:
        PASCOBLEDevice:
            A connected cart if successful.

        None:
            If scanning fails repeatedly or the cart
            cannot be found.
    """

    for attempt in range(1, MAX_SCAN_ATTEMPTS + 1):
        cart = PASCOBLEDevice()

        print(
            f"\nScanning for the Smart Cart "
            f"(attempt {attempt}/{MAX_SCAN_ATTEMPTS})..."
        )

        try:
            devices = cart.scan()

        except PASCOBLEDevice.BLEScanFailed:
            print("Bluetooth scan failed.")

            if attempt < MAX_SCAN_ATTEMPTS:
                print(
                    f"Waiting {SCAN_RETRY_DELAY} seconds "
                    "before trying again..."
                )
                time.sleep(SCAN_RETRY_DELAY)
                continue

            print("\nUnable to start Bluetooth scanning.")
            print("Possible causes:")
            print("  - another Bluetooth scan is already running")
            print("  - BlueZ is temporarily stuck")
            print("  - the BLE adapter is not ready")
            print("  - Blueman or bluetoothctl is using discovery")
            print()
            print("Try checking:")
            print("  bluetoothctl show | grep Discovering")
            print("  hciconfig hci0")

            return None

        selected = next(
            (
                device
                for device in devices
                if TARGET_ID in (device.name or "")
            ),
            None,
        )

        if selected is None:
            print("Scan completed, but the Smart Cart was not found.")

            if attempt < MAX_SCAN_ATTEMPTS:
                print("Make sure the cart is on.")
                print("Waiting before scanning again...")
                time.sleep(SCAN_RETRY_DELAY)
                continue

            print("\nSmart Cart not found.")
            print(
                "Turn it on and confirm that "
                "the Bluetooth light is blinking."
            )

            return None

        print(f"Found: {selected.name}")
        print("Connecting...")

        try:
            cart.connect(selected)

        except Exception as error:
            print(
                f"\nConnection failed: "
                f"{type(error).__name__}"
            )

            try:
                cart.disconnect()
            except Exception:
                pass

            return None

        print(f"Connected to {selected.name}")

        return cart

    return None
