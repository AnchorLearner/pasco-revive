import csv
import os
import time

from pasco import PASCOBLEDevice


TARGET_ID = "795-427"

DATA_DIR = os.path.join("..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

filename = os.path.join(
    DATA_DIR,
    f"cart_run_{time.strftime('%Y%m%d_%H%M%S')}.csv",
)


def main() -> None:
    cart = PASCOBLEDevice()

    try:
        print("Scanning for PASCO devices...")
        devices = cart.scan()

        print("\nDevices found:")
        for device in devices:
            print(f"  - {device.name or 'Unknown'} — {device.address}")

        selected = next(
            (
                device
                for device in devices
                if TARGET_ID in (device.name or "")
            ),
            None,
        )

        if selected is None:
            print(f"\nSmart Cart {TARGET_ID} was not found.")
            print("Make sure the cart is on and its Bluetooth light is blinking.")
            return

        print(f"\nConnecting to {selected.name}...")
        cart.connect(selected)

        print(f"\nSaving data to:\n{filename}\n")
        print("Move the cart. Press Ctrl+C to stop.\n")

        print("Stabilizing position sensor...")

        for _ in range(5):
            cart.read_data("Position")
            time.sleep(0.15)

        initial_position = cart.read_data("Position")
        print(f"Zero position set at: {initial_position:.4f} m")

        start_time = time.monotonic()
        previous_time = start_time
        previous_position = initial_position
        first_sample = True

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    "Time (s)",
                    "Position (m)",
                    "Relative Position (m)",
                    "Velocity (m/s)",
                ]
            )

            while True:
                now = time.monotonic()
                position = cart.read_data("Position")

                elapsed = now - start_time
                dt = now - previous_time
                relative_position = position - initial_position

                if first_sample:
                    velocity = 0.0
                    first_sample = False
                elif dt > 0:
                    velocity = (position - previous_position) / dt
                else:
                    velocity = 0.0

                writer.writerow(
                    [
                        round(elapsed, 3),
                        round(position, 5),
                        round(relative_position, 5),
                        round(velocity, 5),
                    ]
                )

                file.flush()

                print(
                    f"t={elapsed:6.2f}s  "
                    f"Pos={relative_position:8.4f} m  "
                    f"Vel={velocity:8.4f} m/s"
                )

                previous_time = now
                previous_position = position

                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nLogging complete.")

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