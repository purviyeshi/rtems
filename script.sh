#!/bin/bash

# Define variables
BIN_FILE="/home/purva/quick-start/src/rtems/hart-software-services/tools/hss-payload-generator/hello.bin"
BAUD_RATE=115200
EMMC_DEVICE="/dev/sdb"
PASSWORD="2003"
SCREEN_NAME="beagleV-Fire"


# Function to use expect for automating sudo password entry
run_with_sudo() {
    expect -c "
    spawn $1
    expect \"password for $USER:\"
    send \"$PASSWORD\r\"
    interact
    "
}

# Check for required commands
# command -v screen >/dev/null 2>&1 || { echo >&2 "screen command is required but it's not installed. Aborting."; exit 1; }
# command -v dd >/dev/null 2>&1 || { echo >&2 "dd command is required but it's not installed. Aborting."; exit 1; }

# List USB Serial Devices
echo "Listing USB serial devices..."
SERIAL_DEVICE=$(ls /dev | grep -i ttyusb | head -n 1)

if [ -z "$SERIAL_DEVICE" ]; then
    echo "No USB serial devices found. Aborting."
    exit 1
else
    SERIAL_DEVICE="/dev/$SERIAL_DEVICE"
    echo "Using serial device: ${SERIAL_DEVICE}"
fi

# Modify permissions for the serial device
echo "Modifying permissions for ${SERIAL_DEVICE}..."
run_with_sudo "sudo chmod 777 ${SERIAL_DEVICE}"

# --------------------------- OK ^^^^^^ --------------------------- upto give permission --------------------------------

# Start a terminal session with screen and wait for reset
echo "Starting terminal session with ${SERIAL_DEVICE} at baud rate ${BAUD_RATE}. Please press reset on the BeagleV-Fire board now..."
screen -dmS ${SCREEN_NAME} ${SERIAL_DEVICE} ${BAUD_RATE}
# screen ${SERIAL_DEVICE} ${BAUD_RATE}

# Pause to allow user to press reset
echo "Waiting for user to press reset on the BeagleV-Fire board..."
sleep 3  # Adjust the sleep duration as necessary

echo "Press button..."
sleep 10


# Find the screen session
SCREEN_SESSION=$(screen -ls | grep -o '[0-9]*\.beagleV-Fire')

if [ -z "$SCREEN_SESSION" ]; then
    echo "No screen session found. Aborting."
    exit 1
else
    echo "Using screen session: ${SCREEN_SESSION}"
fi

# ------------------------------------------------------------------------------------------------------------

# Send commands to the screen session
echo "Sending HSS commands to the screen session..."
screen -S ${SCREEN_SESSION} -X stuff "MMC\n"
sleep 2
screen -S ${SCREEN_SESSION} -X stuff "USBDMSC\n"
sleep 2

# Load the payload from the host PC
echo "Loading the payload binary to ${EMMC_DEVICE}..."
run_with_sudo "sudo dd if=${BIN_FILE} of=${EMMC_DEVICE} bs=512"

# Close the screen session
# echo "Closing the screen session..."
# screen -S ${SCREEN_SESSION} -X quit

# Reset the BeagleV-Fire board (manual step, cannot be automated easily)
echo "Please reset the BeagleV-Fire board manually and check the output."

# Display completion message
echo "Automation script completed. Check the serial interface for output."


