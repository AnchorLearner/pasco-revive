#!/usr/bin/env bash

echo "==================================="
echo " PASCO Revive - Bluetooth Reset"
echo "==================================="
echo

echo "[1/4] Stopping possible Bluetooth scanner programs..."

pkill -f bluetoothctl 2>/dev/null || true
pkill -f blueman-applet 2>/dev/null || true
pkill -f blueman-tray 2>/dev/null || true

echo "[2/4] Restarting the Bluetooth service..."

sudo systemctl restart bluetooth

echo "[3/4] Waiting for BlueZ..."
sleep 5

echo "[4/4] Resetting BLE adapter hci0..."

sudo hciconfig hci0 down
sleep 3
sudo hciconfig hci0 up

echo
echo "Bluetooth reset complete."
echo "You can now try PASCO Revive again."
