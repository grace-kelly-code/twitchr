# Installation Guide

## Prerequisites

In order to use the Twitchr device application you will need:

1. A Raspberry Pi with Sense Hat attached
2. A USB Webcam or RPI Camera Module
3. A Bluetooth Speaker

This device application is best used in conjunction with the Twitchr Web Application. The installation guide can be found [here](https://github.com/gracielilykelly/twitchr-app/blob/main/docs/InstallationGuide.md).

Twitchr uses the following third parties that you will need credentials for:

1. [Firebase](https://firebase.google.com/?gclid=Cj0KCQiAnNacBhDvARIsABnDa68-eTvFsxp5RIAn5KYARCxjWiYVLHCjL41C-AB4h17VS5RBJfkvdZ8aAvcVEALw_wcB&gclsrc=aw.ds)
2. [HiveMQ](https://www.hivemq.com/)

## Setup Guide

1. With the power off, plug in the Camera
2. Turn the power on and wait for the RPI to boot up
3. Clone this repository onto your Raspberry Pi and cd into it
4. Install the required python libraries via `pip3 install requirements.txt`
5. Populate the `.env` file with your credentials
6. Copy your Firebase `serviceAccountKey.json` file into the twitchr folder
7. In order to play sounds you will need to connect the Raspberry Pi to your Bluetooth speaker. Open the file `/scripts/connect_bluetooth.sh` and replace the placeholder mac address with the mac address of your speaker. If you are not sure of the mac address of your device you can find it by running `sudo bluetoothctl paired-devices` or if is not paired you can run `sudo bluetoothctl scan on`
8. Place the Bluetooth speaker and webcam near the bird feeder
9. To run the MQTT client open a new terminal window and type `python3 mqtty.py` This will connect via the credentials you have provided in the `env` file and listen for a payload of data to the `twitchr` topic.
10. In a new terminal window run the following command - `python3 main.py`. This will start capturing images and running them through the detector and classifier and store images on firebase. Once you have the Twitchr Web App setup and the credentials set in the `env` file you should receive messages in the MQTT queue and also notifications
