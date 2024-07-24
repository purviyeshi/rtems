#!/bin/bash

# Define variables
BIN_FILE="/home/purva/quick-start/src/rtems/hart-software-services/tools/hss-payload-generator/hello.bin"
SERIAL_DEVICE="/dev/ttyUSB0"
BAUD_RATE=115200
EMMC_DEVICE="/dev/sdb"

# Check for required commands
command -v screen >/dev/null 2>&1 || { echo >&2 "screen command is required but it's not installed. Aborting."; exit 1; }
command -v dd >/dev/null 2>&1 || { echo >&2 "dd command is required but it's not installed. Aborting."; exit 1; }

# List USB Serial Devices
echo "Listing USB serial devices..."
ls /dev | grep -i ttyusb

# Modify permissions for the serial device
echo "Modifying permissions for ${SERIAL_DEVICE}..."
sudo chmod 777 ${SERIAL_DEVICE}

# Start a terminal session with screen
echo "Starting terminal session with ${SERIAL_DEVICE} at baud rate ${BAUD_RATE}..."
screen -dmS beagleV-Fire ${SERIAL_DEVICE} ${BAUD_RATE}

# Waiting to start the screen session
sleep 3

# Send commands to the screen session
echo "Sending HSS commands to the screen session..."
screen -S beagleV-Fire -X stuff "MMC\r"
sleep 1
screen -S beagleV-Fire -X stuff "USBDMSC\r"
sleep 1

# Load the payload from the host PC
echo "Loading the payload binary to ${EMMC_DEVICE}..."
sudo dd if=${BIN_FILE} of=${EMMC_DEVICE} bs=512

# Close the screen session
echo "Closing the screen session..."
screen -S beagleV-Fire -X quit

# Reset the BeagleV-Fire board (manual step, cannot be automated easily)
echo "Please reset the BeagleV-Fire board manually and check the output."

# Display completion message
echo "Automation script completed. Check the serial interface for output."

