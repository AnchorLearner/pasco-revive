import time
from statistics import mean
from pasco import PASCOBLEDevice


TARGET_ID = "795-427"
TARE_SAMPLES = 20


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

        print("Keep the force hook completely unloaded.")
        print("Calculating zero offset...")

        samples = []
        for _ in range(TARE_SAMPLES):
            samples.append(cart.read_data("Force"))
            time.sleep(0.1)

        force_offset = mean(samples)

        print(f"Measured offset: {force_offset:.3f} N")
        print("Tare complete. Press Ctrl+C to stop.\n")

        while True:
            raw_force = cart.read_data("Force")
            corrected_force = raw_force - force_offset

            print(
                f"Raw: {raw_force:7.3f} N | "
                f"Tared: {corrected_force:7.3f} N"
            )

            time.sleep(0.2)

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
