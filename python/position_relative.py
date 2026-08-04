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

        initial_position = cart.read_data("Position")

        print(f"Initial position: {initial_position:.4f} m")
        print("Relative position is now zero.")
        print("Move the cart left and right. Press Ctrl+C to stop.\n")

        while True:
            raw_position = cart.read_data("Position")
            relative_position = raw_position - initial_position

            print(
                f"Raw: {raw_position:8.4f} m | "
                f"Relative: {relative_position:8.4f} m"
            )

            time.sleep(0.1)

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
