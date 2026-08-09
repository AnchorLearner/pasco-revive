from pasco import PASCOBLEDevice


TARGET_ID = "795-427"


def connect_cart():
    cart = PASCOBLEDevice()

    print("\nScanning for the Smart Cart...")
    devices = cart.scan()

    selected = next(
        (
            device
            for device in devices
            if TARGET_ID in (device.name or "")
        ),
        None,
    )

    if selected is None:
        print("\nSmart Cart not found.")
        print("Turn it on and confirm that the Bluetooth light is blinking.")
        return None

    print(f"Connecting to {selected.name}...")
    cart.connect(selected)

    return cart
