import time
from pasco import PASCOBLEDevice

TARGET_ID = "795-427"


def main():
    cart = PASCOBLEDevice()

    devices = cart.scan()

    selected = next(
        d for d in devices
        if TARGET_ID in (d.name or "")
    )

    cart.connect(selected)

    print("Roll the cart forward and backward.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            position = cart.read_data("Position")
            print(f"Position: {position:.4f} m")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopped.")

    finally:
        cart.disconnect()


if __name__ == "__main__":
    main()
