from pasco import PASCOBLEDevice


TARGET_ID = "795-427"


def main() -> None:
    cart = PASCOBLEDevice()

    try:
        print("Scanning for PASCO devices...")
        devices = cart.scan()

        if not devices:
            print("No PASCO devices found.")
            return

        print("\nDevices found:")
        selected = None

        for index, device in enumerate(devices):
            name = device.name or "Unknown"
            address = getattr(device, "address", "Unknown")
            print(f"{index}: {name} — {address}")

            if TARGET_ID in name:
                selected = device

        if selected is None:
            print(f"\nNo device containing ID {TARGET_ID} was found.")
            return

        print(f"\nConnecting to {selected.name}...")
        cart.connect(selected)
        print("Connected successfully.")

        print("\nSensors:")
        for sensor in cart.get_sensor_list():
            print(f"  - {sensor}")

        print("\nMeasurements:")
        for measurement in cart.get_measurement_list():
            try:
                unit = cart.get_measurement_unit(measurement)
            except Exception:
                unit = "unknown"

            print(f"  - {measurement}: {unit}")

    except Exception as error:
        print(f"\nFailure type: {type(error).__name__}")
        print(f"Failure details: {error!r}")

    finally:
        try:
            cart.disconnect()
        except Exception:
            pass

        print("\nDisconnected.")


if __name__ == "__main__":
    main()
