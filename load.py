import subprocess
import time

import ctypes

# Define variables
BIN_FILE = "/home/purva/quick-start/src/rtems/hart-software-services/tools/hss-payload-generator/hello.bin"
EMMC_DEVICE = "/dev/sdb"
PASSWORD = "2003"

# Function to execute a shell command and get the output
def execute_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(result.stderr)
        return None
    return result.stdout.strip()

# Check for active screen session
print("Checking for active screen sessions...")
screen_output = execute_command("screen -ls")
if screen_output is None:
    print("Error checking screen sessions. Aborting.")
    exit(1)

# Find the screen session
SCREEN_SESSION = None
for line in screen_output.split('\n'):
    if '.purva-IdeaPad-Gaming-3-15IHU6' in line:
        SCREEN_SESSION = line.split('.')[0]
        break

if SCREEN_SESSION is None:
    print("No active screen session found. Aborting.")
    exit(1)
else:
    print(f"Using screen session: {SCREEN_SESSION}")

# Function to send commands to the screen session
def send_to_screen(session, command):
    subprocess.run(f"screen -S {session} -X stuff '{command}\\n'", shell=True)
    time.sleep(2)  # Wait for 2 seconds between commands

# Send commands to the screen session
print("Sending HSS commands to the screen session...")
send_to_screen(SCREEN_SESSION, "MMC")
send_to_screen(SCREEN_SESSION, "USBDMSC")

# Load the payload from the host PC
print(f"Loading the payload binary to {EMMC_DEVICE}...")
dd_command = f"echo {PASSWORD} | sudo -S dd if={BIN_FILE} of={EMMC_DEVICE} bs=512"
print(f"Executing command: {dd_command}")
result = execute_command(dd_command)
if result is None:
    print("Error loading the payload. Aborting.")
    exit(1)

time.sleep(10)  # Wait for 10 seconds






## ----------------- reset code part ----------------- ##


# Define HSS_HART_ALL constant
HSS_HART_ALL = 5

# Load the shared library
reset_lib = ctypes.CDLL('./libreset.so')


# Define the function argument and return types
reset_lib.HSS_reboot_cold.argtypes = [ctypes.c_int]
reset_lib.HSS_reboot_cold.restype = None

# Call the reset function with HSS_HART_ALL
reset_lib.HSS_reboot_cold(ctypes.c_int(HSS_HART_ALL))
