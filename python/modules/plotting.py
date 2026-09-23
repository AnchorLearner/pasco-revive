import time

import matplotlib.pyplot as plt

from modules.connection import connect_cart, disconnect_cart


def live_plot() -> None:
    cart = None

    try:
        cart = connect_cart()

        if cart is None:
            return

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
        print("Close the graph window or press Ctrl+C to return to the menu.")

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
        print("\nStopping live plot.")

    except Exception as error:
        print(f"\nCould not read the Smart Cart: {type(error).__name__}")
        print(
            "Make sure the cart is on and "
            "no other Bluetooth program is using it."
        )

    finally:
        plt.ioff()
        plt.close("all")

        disconnect_cart(cart)

        print("Disconnected.")
        print("Disconnected.")
