import time

import matplotlib.pyplot as plt
from pasco import PASCOBLEDevice


TARGET_ID = "795-427"


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

        times = []
        positions = []

        start_time = time.monotonic()

        plt.ion()

        figure, axis = plt.subplots()
        line, = axis.plot([], [])

        axis.set_title("PASCO Smart Cart Live Position")
        axis.set_xlabel("Time (s)")
        axis.set_ylabel("Relative Position (m)")
        axis.grid(True)

        print("Move the cart left and right.")
        print("Close the graph window or press Ctrl+C to stop.")

        while plt.fignum_exists(figure.number):
            current_time = time.monotonic() - start_time
            position = cart.read_data("Position")
            relative_position = position - initial_position

            times.append(current_time)
            positions.append(relative_position)

            line.set_data(times, positions)

            axis.relim()
            axis.autoscale_view()

            figure.canvas.draw()
            figure.canvas.flush_events()

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

        plt.ioff()
        plt.close("all")
        print("Disconnected.")


if __name__ == "__main__":
    main()