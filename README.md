# PASCO Revive

PASCO Revive is a Linux and Python project for restoring, investigating, and reusing discarded PASCO wireless scientific devices.

The project began after several PASCO devices that appeared to be defective were found to contain failed lithium-polymer batteries. Replacing a failed battery with a known-good compatible battery showed that the electronics in multiple devices were still functional.

PASCO Revive combines hardware troubleshooting with Linux, Bluetooth Low Energy (BLE), Python, sensor data acquisition, visualization, and experimental data logging.

## Project discovery

Several discarded PASCO Smart Carts and a Wireless Smart Gate initially appeared to be defective.

Inspection revealed swollen or failed 3.7 V lithium-polymer batteries. Testing with a known-good battery caused multiple devices to power up and advertise normally over Bluetooth.

This suggested that at least some apparently failed scientific instruments may have functional electronics and sensors but unusable batteries.

The project currently explores:

- electronics troubleshooting;
- battery-failure analysis;
- Ubuntu Linux;
- Bluetooth Low Energy;
- Python sensor access;
- multi-device discovery;
- CSV data logging;
- live data visualization;
- scientific instrument recovery and reuse.

## Tested Smart Carts

Two recovered PASCO Smart Carts have been tested with the Python application.

### Smart Cart 1

- Device ID: `795-427`
- BLE name: `Smart Cart 795-427>58`

### Smart Cart 2

- Device ID: `330-794`
- BLE name: `Smart Cart 330-794>5M`

Both carts can be discovered simultaneously. When more than one Smart Cart is available, PASCO Revive displays the detected carts and allows the user to select which device to use.

## Confirmed measurements

Measurements accessible from the Smart Cart include:

- Force
- Position
- Acceleration X, Y, and Z
- Resultant acceleration
- Angular velocity X, Y, and Z

## Current application

Run the application from the `python` directory:

```bash
python app.py
```

The current menu provides:

```text
===================================
         PASCO Revive
===================================
1. Live Force
2. Live Position
3. Live Plot
4. Record Experiment
5. Exit
```

All four measurement modes have been tested successfully with both recovered Smart Carts.

## Current capabilities

PASCO Revive can currently:

- scan for Smart Carts over BLE;
- discover multiple Smart Carts;
- allow interactive device selection;
- retry failed Bluetooth scans;
- connect and disconnect safely;
- read live force measurements;
- calculate a software force tare;
- read absolute and relative position;
- calculate velocity from position measurements;
- display a live position graph;
- record experiments to CSV;
- return safely to the main menu after measurements.

## Force sensor offsets

The two recovered carts show different unloaded raw force offsets.

Observed examples were approximately:

- Smart Cart `795-427`: about `-4.4 N`
- Smart Cart `330-794`: about `-2.3 N`

Because the raw offsets differ between devices, PASCO Revive calculates a force offset for the selected cart at the beginning of a measurement session rather than relying on a universal correction value.

After software tare, unloaded force measurements are typically close to zero.

These values are experimental observations from the recovered devices and should not be interpreted as factory calibration specifications.

## Experiment logging

The experiment logger records data including:

```text
Time (s)
Position (m)
Relative Position (m)
Velocity (m/s)
Raw Force (N)
Tared Force (N)
```

Experiment files are stored in:

```text
data/
```

with timestamped filenames such as:

```text
cart_run_YYYYMMDD_HHMMSS.csv
```

## Bluetooth reliability

Linux BLE scanning can occasionally fail when BlueZ believes another discovery operation is active or when another Bluetooth application is using the adapter.

PASCO Revive includes scan retry handling and reports these failures without crashing the application.

A Bluetooth recovery utility is also provided:

```text
python/scripts/reset_bluetooth.sh
```

It can be run from the project root with:

```bash
./python/scripts/reset_bluetooth.sh
```

The script stops common competing Bluetooth scanner processes, restarts the Linux Bluetooth service, and resets the BLE adapter used during development.

Because the script restarts system Bluetooth services and uses `sudo`, it should be run manually rather than automatically by the measurement application.

## Recovered Wireless Smart Gate

A PASCO Wireless Smart Gate was also recovered during the hardware investigation.

The gate initially appeared nonfunctional, but it powered up and advertised normally when tested with a known-good compatible battery.

The Smart Gate is therefore considered recovered hardware, but it has **not yet been integrated into the PASCO Revive Python application**.

Future Smart Gate support could enable comparison between:

- cart encoder measurements;
- optical timing measurements;
- calculated velocity;
- timing accuracy;
- sensor latency;
- wheel slip;
- measurement repeatability.

## Project structure

```text
pasco-revive/
├── data/
├── docs/
├── images/
├── notebooks/
├── python/
│   ├── app.py
│   ├── modules/
│   │   ├── connection.py
│   │   ├── force.py
│   │   ├── logger.py
│   │   ├── plotting.py
│   │   └── position.py
│   └── scripts/
│       └── reset_bluetooth.sh
├── README.md
├── .gitignore
└── requirements.txt
```

Additional experimental and diagnostic Python scripts may also be present in the `python/` directory.

## Project direction

PASCO Revive is evolving from a hardware-recovery experiment into a small open scientific-instrumentation toolkit.

Future work may include:

- Wireless Smart Gate support;
- synchronized measurements from multiple devices;
- comparison of independent measurement methods;
- calibration and repeatability experiments;
- automated analysis and plotting of recorded experiments;
- investigation of additional discarded PASCO devices;
- documentation of common hardware failure modes.

The longer-term goal is to explore how discarded scientific instruments can be characterized, restored, validated, and reused using open software and accessible electronics tools.

## Safety

Swollen lithium-polymer batteries can present a fire hazard.

Damaged or swollen cells should not be charged, punctured, crushed, bent, or reused. Battery replacement work should account for cell chemistry, voltage, connector polarity, physical dimensions, and any additional temperature-sensing or protection connections.