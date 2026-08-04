import csv
import os
import time
from statistics import mean

from pasco import PASCOBLEDevice


TARGET_ID = "795-427"
TARE_SAMPLES = 20

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

        selected = next(
            (
                device
                for device in devices
                if TARGET_ID in (device.name or "")
            ),
            None,
        )

        if selected is None:
            print(f"Smart Cart {TARGET_ID} was not found.")
            return

        print(f"Connecting to {selected.name}...")
        cart.connect(selected)

        print("Stabilizing position sensor...")
        for _ in range(5):
            cart.read_data("Position")
            time.sleep(0.15)

        initial_position = cart.read_data("Position")

        print("Do not press the force sensor.")
        print("Calculating force offset...")

        force_samples = []
        for _ in range(TARE_SAMPLES):
            force_samples.append(cart.read_data("Force"))
            time.sleep(0.1)

        force_offset = mean(force_samples)

        print(f"Position zero: {initial_position:.4f} m")
        print(f"Force offset: {force_offset:.3f} N")
        print(f"Saving data to: {filename}")
        print("Move or press the cart. Press Ctrl+C to stop.\n")

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
                    "Raw Force (N)",
                    "Tared Force (N)",
                ]
            )

            while True:
                now = time.monotonic()

                position = cart.read_data("Position")
                raw_force = cart.read_data("Force")

                elapsed = now - start_time
                dt = now - previous_time

                relative_position = position - initial_position
                tared_force = raw_force - force_offset

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
                        round(raw_force, 3),
                        round(tared_force, 3),
                    ]
                )

                file.flush()

                print(
                    f"t={elapsed:6.2f}s | "
                    f"Pos={relative_position:8.4f} m | "
                    f"Vel={velocity:8.4f} m/s | "
                    f"Force={tared_force:7.3f} N"
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
