#!/bin/bash

# Get the local network interface (e.g., wlan0 for Wi-Fi). Adjust as necessary.
INTERFACE="wlp0s20f3"

# Scan the local network and count the results. Subtract 1 to exclude the local device.
DEVICES=$(sudo arp-scan -I $INTERFACE --localnet | grep -E '([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}' | wc -l)
DEVICES=$((DEVICES - 1))

echo "Number of devices connected to Wi-Fi (excluding this device): $DEVICES"
