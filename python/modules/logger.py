import csv
import os
import time
from statistics import mean

from modules.connection import connect_cart, disconnect_cart


TARE_SAMPLES = 20


def record_experiment() -> None:
    cart = None

    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "data",
    )

    os.makedirs(data_dir, exist_ok=True)

    filename = os.path.join(
        data_dir,
        f"cart_run_{time.strftime('%Y%m%d_%H%M%S')}.csv",
    )

    try:
        cart = connect_cart()

        if cart is None:
            return

        print("Stabilizing position sensor...")

        for _ in range(5):
            cart.read_data("Position")
            time.sleep(0.15)

        initial_position = cart.read_data("Position")

        print("Do not touch the force sensor.")
        print("Calculating force offset...")

        force_samples = []

        for _ in range(TARE_SAMPLES):
            force_samples.append(cart.read_data("Force"))
            time.sleep(0.1)

        force_offset = mean(force_samples)

        print(f"Position zero: {initial_position:.4f} m")
        print(f"Force offset: {force_offset:.3f} N")
        print(f"\nSaving experiment to:\n{filename}")
        print("\nMove the cart or apply force.")
        print("Press Ctrl+C to stop recording.\n")

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
        print("\nRecording stopped.")

    except Exception as error:
        print(f"\nCould not record experiment: {type(error).__name__}")
        print(
            "Make sure the cart is on and "
            "no other Bluetooth program is using it."
        )

    finally:
        disconnect_cart(cart)
        print("Disconnected.")