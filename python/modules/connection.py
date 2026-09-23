import time

from pasco import PASCOBLEDevice


MAX_SCAN_ATTEMPTS = 3
SCAN_RETRY_DELAY = 3


def connect_cart():
    """
    Scan for nearby PASCO Smart Carts, allow the user to select one,
    and connect to the selected cart.

    Returns:
        PASCOBLEDevice:
            A connected Smart Cart.

        None:
            If scanning fails, no carts are found,
            or the user cancels selection.
    """

    for attempt in range(1, MAX_SCAN_ATTEMPTS + 1):
        cart = PASCOBLEDevice()

        print(
            f"\nScanning for Smart Carts "
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
            return None

        smart_carts = [
            device
            for device in devices
            if "Smart Cart" in (device.name or "")
        ]

        if not smart_carts:
            print("Scan completed, but no Smart Carts were found.")

            if attempt < MAX_SCAN_ATTEMPTS:
                print("Make sure a cart is on.")
                print("Waiting before scanning again...")
                time.sleep(SCAN_RETRY_DELAY)
                continue

            print("\nNo Smart Carts found.")
            print(
                "Turn on a cart and confirm that "
                "its Bluetooth light is blinking."
            )
            return None

        break

    print("\nSmart Carts found:\n")

    for number, device in enumerate(smart_carts, start=1):
        print(f"  {number}. {device.name}")

    if len(smart_carts) == 1:
        selected = smart_carts[0]
        print(f"\nAutomatically selecting {selected.name}")

    else:
        while True:
            choice = input(
                "\nSelect a cart number "
                "or enter Q to cancel: "
            ).strip()

            if choice.lower() == "q":
                print("Connection cancelled.")
                return None

            try:
                selection = int(choice)

                if 1 <= selection <= len(smart_carts):
                    selected = smart_carts[selection - 1]
                    break

            except ValueError:
                pass

            print("Invalid selection. Try again.")

    print(f"\nConnecting to {selected.name}...")

    try:
        cart.connect(selected)

    except Exception as error:
        print(
            f"Connection failed: "
            f"{type(error).__name__}: {error}"
        )

        try:
            cart.disconnect()
        except Exception:
            pass

        return None

    print(f"Connected to {selected.name}")

    return cart


def disconnect_cart(cart) -> None:
    """
    Safely disconnect a Smart Cart without allowing
    shutdown errors to crash the main application.
    """

    if cart is None:
        return

    try:
        cart.disconnect()

    except KeyboardInterrupt:
        pass

    except Exception as error:
        print(
            f"Warning: disconnect did not finish cleanly: "
            f"{type(error).__name__}"
        )
