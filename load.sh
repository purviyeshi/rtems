#!/bin/bash

# Define variables
BIN_FILE="/home/purva/quick-start/src/rtems/hart-software-services/tools/hss-payload-generator/hello.bin"
EMMC_DEVICE="/dev/sdb"
PASSWORD="2003"

# Check for active screen session
echo "Checking for active screen sessions..."
SCREEN_SESSION=$(screen -ls | grep -oP '\d+\.pts-\d+\.purva-IdeaPad-Gaming-3-15IHU6' | head -n 1)

if [ -z "$SCREEN_SESSION" ]; then
    echo "No active screen session found. Aborting."
    exit 1
else
    echo "Using screen session: ${SCREEN_SESSION}"
fi

# Send commands to the screen session
echo "Sending HSS commands to the screen session..."

screen -S ${SCREEN_SESSION} -X stuff "MMC\n"
sleep 2
screen -S ${SCREEN_SESSION} -X stuff "USBDMSC\n"
sleep 2

# Load the payload from the host PC
echo "Loading the payload binary to ${EMMC_DEVICE}..."
echo $PASSWORD | sudo -S dd if=${BIN_FILE} of=${EMMC_DEVICE} bs=512

sleep 10
screen -S ${SCREEN_SESSION} -X stuff "RESET\n"

