#!/bin/bash
# Author: Grace Kelly
# Description: Connect to a specified bluetooth device

# Set your device mac address here
# to get paired devices run the following:
# sudo bluetoothctl paired-devices
device_mac=00000000

echo "Connecting to Bluetooth device..."
pulseaudio --start
sudo bluetoothctl default-agent
if sudo bluetoothctl connect $device_mac ;
then  
    echo "Connected to device ${device_mac}"
fi