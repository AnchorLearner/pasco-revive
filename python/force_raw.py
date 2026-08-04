import time
from pasco import PASCOBLEDevice


TARGET_ID = "795-427"


def main() -> None:
    cart = PASCOBLEDevice()

    try:
        print("Scanning...")
        devices = cart.scan()

        selected = next(
            (device for device in devices if TARGET_ID in (device.name or "")),
            None,
        )

        if selected is None:
            print(f"Smart Cart {TARGET_ID} not found.")
            return

        print(f"Connecting to {selected.name}...")
        cart.connect(selected)
        print("Connected. Move the cart. Press Ctrl+C to stop.\n")

        while True:
            force = cart.read_data("Force")
            print(f"Force: {force} N")
            time.sleep(0.25)

    except KeyboardInterrupt:
        print("\nStopped by user.")

    except Exception as error:
        print(f"\nError: {type(error).__name__}: {error!r}")

    finally:
        try:
            cart.disconnect()
        except Exception:
            pass

        print("Disconnected.")


if __name__ == "__main__":
    main()
