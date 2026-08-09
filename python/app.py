from modules.logger import record_experiment
from modules.plotting import live_plot
from modules.position import live_position
from modules.force import live_force
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run_script(filename: str) -> None:
    script_path = SCRIPT_DIR / filename

    if not script_path.exists():
        print(f"\nCould not find: {script_path}")
        return

    print(f"\nStarting {filename}...")
    print("Press Ctrl+C inside the selected program to stop it.\n")

    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            check=False,
        )
    except KeyboardInterrupt:
        print("\nReturning to the main menu.")


def main() -> None:

    while True:
        print("\n===================================")
        print("         PASCO Revive")
        print("===================================")
        print("1. Live Force")
        print("2. Live Position")
        print("3. Live Plot")
        print("4. Record Experiment")
        print("5. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            live_force()
        elif choice == "2":
            live_position()
        elif choice == "3":
            live_plot()
        elif choice == "4":
            record_experiment()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid option. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
