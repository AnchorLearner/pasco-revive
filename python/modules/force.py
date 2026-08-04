import time
from statistics import mean

from pasco import PASCOBLEDevice


TARGET_ID = "795-427"
TARE_SAMPLES = 20


def live_force() -> None:
    cart = PASCOBLEDevice()

    try:
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
            return

        print(f"Connecting to {selected.name}...")
        cart.connect(selected)

        print("\nDo not touch the force sensor.")
        print("Calculating zero offset...")

        samples = []

        for _ in range(TARE_SAMPLES):
            samples.append(cart.read_data("Force"))
            time.sleep(0.1)

        force_offset = mean(samples)

        print(f"Measured offset: {force_offset:.3f} N")
        print("Live force started. Press Ctrl+C to return to the menu.\n")

        while True:
            raw_force = cart.read_data("Force")
            tared_force = raw_force - force_offset

            print(
                f"Raw: {raw_force:7.3f} N | "
                f"Tared: {tared_force:7.3f} N"
            )

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nStopping live force.")

    except Exception as error:
        print(f"\nCould not read the Smart Cart: {type(error).__name__}")
        print("Make sure the cart is on and no other Bluetooth program is using it.")

    finally:
        try:
            cart.disconnect()
        except Exception:
            pass

        print("Disconnected.")
