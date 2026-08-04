# PASCO Revive

PASCO Revive is a Linux and Python project for restoring and reusing discarded PASCO wireless scientific devices.

## Project discovery

Several PASCO Smart Carts and a Wireless Smart Gate appeared to be defective. Testing with a known-good battery showed that the devices were still functional and that their original lithium-polymer batteries had failed.

The project now combines:

- electronics troubleshooting;
- battery-failure analysis;
- Ubuntu Linux;
- Bluetooth Low Energy;
- Python sensor access;
- CSV data logging;
- live data visualization.

## Tested device

- PASCO Smart Cart
- Device ID: `795-427`
- BLE name: `Smart Cart 795-427>58`

## Confirmed measurements

- Force
- Position
- Acceleration X, Y, and Z
- Resultant acceleration
- Angular velocity X, Y, and Z

## Current capabilities

- Scan for PASCO BLE devices
- Connect to the Smart Cart
- List sensors and measurements
- Read live force data
- Tare the force sensor in software
- Read relative position
- Calculate velocity
- Save data to CSV
- Display a live position graph

## Project structure

```text
pasco-revive/
├── data/
├── docs/
├── images/
├── notebooks/
├── python/
├── README.md
└── requirements.txt