import time

from modules.connection import connect_cart


def live_position() -> None:
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

        print(f"Position zero set at {initial_position:.4f} m")
        print("Move the cart left and right.")
        print("Press Ctrl+C to return to the menu.\n")

        while True:
            raw_position = cart.read_data("Position")
            relative_position = raw_position - initial_position

            print(
                f"Raw: {raw_position:8.4f} m | "
                f"Relative: {relative_position:8.4f} m"
            )

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping live position.")

    except Exception as error:
        print(f"\nCould not read the Smart Cart: {type(error).__name__}")
        print(
            "Make sure the cart is on and "
            "no other Bluetooth program is using it."
        )

    finally:
        if cart is not None:
            try:
                cart.disconnect()
            except Exception:
                pass

        print("Disconnected.")
