# PASCO Revive — Bluetooth Investigation Journal

**Date:** November 20, 2026  
**Project:** PASCO Revive  
**Device:** PASCO Wireless Smart Gate (PS-3225)  
**Status:** Bluetooth connection successful; beam-data protocol not yet decoded.

## 1. Why We Started This Investigation

The goal of PASCO Revive is to restore useful scientific equipment and develop Python software to communicate with it.

We already have a working Python application for PASCO Smart Carts.

Our next goal is to support the PASCO Wireless Smart Gate, which uses two optical beams to measure the motion of objects passing through it.

We want to develop our own software that can:

- Connect to the Smart Gate.
- Detect when its optical beams are blocked or cleared.
- Record event timestamps.
- Calculate speed and other motion measurements.
- Export experimental data to CSV.

## 2. What Is Bluetooth Low Energy?

Bluetooth Low Energy (BLE) is a wireless communication technology used by sensors and other electronic devices.

Our Ubuntu computer communicates with the Smart Gate through BLE.

Important concepts:

**BLE scanning:** Searching for nearby Bluetooth devices.

**BLE connection:** Establishing communication with a particular device.

**GATT service:** A group of related Bluetooth functions.

**GATT characteristic:** A communication point within a service.

**Read:** Requesting information stored in a characteristic.

**Write:** Sending information or a command to a characteristic.

**Notify:** Receiving messages from a characteristic when the device sends them.

**UUID:** A unique identifier used to identify a Bluetooth service or characteristic.

These concepts are important because the Smart Gate does not simply send measurements automatically when we connect.

We must determine how to configure it to report measurements.

## 3. Our Ubuntu Experiments

We used Ubuntu, Python, and the Bleak Bluetooth library.

Our experiments included:

### Scanning

We used Python to search for nearby BLE devices.

**Result:** Ubuntu successfully discovered the Wireless Smart Gate.

### Examining GATT Services

We examined the Smart Gate's Bluetooth services and characteristics.

We identified two important services:

- Device service: `4a5c0000-0000-0000-0000-5c1e741f1c00`
- Sensor service: `4a5c0001-0000-0000-0000-5c1e741f1c00`

Some characteristics support reading, others support writing, and others support notifications.

**Result:** We identified possible communication paths, but not yet the commands needed for beam measurements.

### Connecting with Python

We created and tested `smart_gate_raw.py`.

The script successfully connected to the new Smart Gate and subscribed to available notification characteristics.

**Result:** Python can establish a BLE connection and receive notifications.

### Sending an Experimental Command

We sent the hexadecimal bytes:

`05 03`

The first byte corresponds to a one-sample request command used elsewhere in the installed PASCO Python library.

The second byte was chosen because the Smart Gate's documented `Blocked` and `TimeStamp` fields occupy three bytes in total.

We received a response beginning:

`c0 00 05`

This is consistent with a successful result response for command `05`, according to the library's response-handling logic.

**Important:** This does not prove that the remaining response bytes contain beam measurements.

Blocking and clearing the optical beams did not produce identifiable beam-event notifications during our test.

## 4. Using btmon on Ubuntu

We used `btmon`, a Linux Bluetooth monitoring tool, to record communication between Ubuntu and the Smart Gate.

Example command:

`sudo btmon -i 0 -w capture.btsnoop`

Explanation:

- `sudo`: Run with administrator privileges.
- `btmon`: Monitor Bluetooth activity.
- `-i 0`: Monitor Bluetooth adapter `hci0`.
- `-w`: Write the captured traffic to a file.
- `capture.btsnoop`: The output filename.

We later decoded the capture into readable text.

The capture confirmed that:

- Ubuntu sent `05 03` to a sensor-service characteristic.
- The Smart Gate returned `c0 00 05 0e 00 00`.
- Other notifications were received, including messages beginning with `85`.

The meaning of the `85` notifications remains unknown.

**Lesson:** A Bluetooth capture records what was transmitted. It does not automatically explain what the bytes mean.

## 5. Investigating the Installed PASCO Python Library

We examined the installed package's source code without modifying it.

Two useful Linux commands were:

`grep`: Search files for matching text.

`sed`: Display selected lines of a text file.

We found that the Smart Gate uses interface ID `1048`.

Its interface definition lists four channels with type `CIDigital`.

Only channel 0 explicitly identifies sensor ID `2055`.

The sensor definition describes two measurements:

| Measurement | Data size | Unit |
| --- | --- | --- |
| Blocked | 1 byte | Unitless |
| TimeStamp | 2 bytes | Microseconds |

The datasheet lists a default rate of 20 Hz and a maximum rate of 50 Hz.

However, the installed library's normal sensor-initialization routine selects channels of type `Pasport`, not `CIDigital`.

Searching the installed Python package showed that `CIDigital` appears in device descriptions but not in an identifiable implementation of its measurement protocol.

**Conclusion:** The package contains useful Smart Gate descriptions but does not provide a clear working method for reading its beam events.

## 6. Testing PASCO Capstone on Windows 10

We used a second computer running Windows 10 and PASCO Capstone.

Capstone successfully connected to the new Wireless Smart Gate.

We recorded measurements and exported a CSV file.

The exported measurements included separate state channels and timing information.

**Result:** The Smart Gate works with official PASCO software and can provide measurement data.

This is important because it confirms that the remaining difficulty is in our Python communication method, rather than a demonstrated failure of the new gate.

## 7. Investigating Windows Bluetooth Diagnostics

We examined Windows 10's built-in diagnostic tools.

Commands included:

`netsh trace show scenarios`

This listed available tracing scenarios.

`logman query providers`

This listed Windows diagnostic event providers.

`wevtutil`

This allowed us to inspect information about Bluetooth event-log channels.

We identified the channel:

`Microsoft-Windows-BTH-BTHPORT/HCI`

HCI stands for Host Controller Interface.

However, we did not establish whether this Windows channel exposes the raw BLE characteristic writes needed to reproduce Capstone's communication.

**Important:** We did not complete a successful Bluetooth packet capture of Capstone.

## 8. What We Know and What We Do Not Know

### Confirmed

- The new Smart Gate's optical beams respond physically.
- Ubuntu discovers and connects to the gate.
- Python can subscribe to BLE notifications.
- We captured Bluetooth traffic using `btmon`.
- The device identifies as interface `1048`.
- The datasheet identifies four `CIDigital` channels.
- Sensor `2055` describes `Blocked` and `TimeStamp` fields.
- PASCO Capstone successfully records measurements.

### Not Yet Known

- The exact BLE command sequence used by Capstone to start measurements.
- How the four digital channels map to physical inputs and functions.
- How beam transitions are encoded in Bluetooth messages.
- How the two-byte timestamp field should be interpreted.
- Whether our experimental `05 03` request is appropriate for this device.

We must not present guesses as established protocol facts.

## 9. Next Development Goal

Our next task is to build a separate Python application:

`python/smart_gate_monitor.py`

The first version should:

1. Connect to the Smart Gate.
2. Display connection status.
3. Show incoming BLE notifications.
4. Save raw notifications to CSV.
5. Keep the existing Smart Cart application unchanged.

Later, once the protocol is understood, we can add beam-state displays, timestamps, speed calculations, and graphs.

## 10. Lessons Learned

This investigation taught us that:

- Connecting to a Bluetooth device is different from understanding its measurements.
- A datasheet can describe measurements without documenting the communication protocol.
- Reading existing source code is an important development skill.
- Bluetooth captures provide evidence, but interpreting that evidence requires additional work.
- Official software can provide a reference for expected behavior.
- Failed or incomplete experiments are worth documenting.
- Understanding each command is more valuable than copying commands without knowing their purpose.

**Project principle: Understand → Execute → Observe → Explain → Save.**
