# This python script generate binary files of the whole testsuits 


import os
import shutil


## ----------------- check folders in testsuits ----------------- ##

# Define the path to the testsuites directory
testsuites_path = 'build/riscv/beaglevfire/testsuites'

# Define the output file
output_file = 'directory_names.txt'

# Open the output file in write mode
with open(output_file, 'w') as file:
    # Iterate through each item in the testsuites directory
    for item in os.listdir(testsuites_path):
        item_path = os.path.join(testsuites_path, item)
        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Write the directory name to the file
            file.write(f"{item}\n")

print(f"Directory names have been written to {output_file}")





## ----------------- This whill generate a file that contains path of each executatable file with serial number ----------------- ##

# Define the path to the testsuites directory
testsuites_path = os.path.abspath('build/riscv/beaglevfire/testsuites')

# Define the output file for directory names
directory_file = 'directory_names.txt'
# Define the output file for executable file paths
exe_list_file = 'exe_paths.txt'

# Get directory names
directories = []
with open(directory_file, 'r') as file:
    directories = [line.strip() for line in file]

# Open the output file for executable file paths in write mode
with open(exe_list_file, 'w') as file:
    exe_counter = 1  # Initialize a counter for numbering executables
    # Iterate through each directory name
    for directory in directories:
        dir_path = os.path.join(testsuites_path, directory)
        if os.path.isdir(dir_path):
            # Write the directory name to the file
            file.write(f"Directory: {dir_path}\n")
            # List the .exe files in the directory
            exe_files = [item for item in os.listdir(dir_path) if item.endswith('.exe')]
            if exe_files:
                # Write the full path of each .exe file with a unique number
                for exe_file in exe_files:
                    exe_path = os.path.abspath(os.path.join(dir_path, exe_file))
                    file.write(f"{exe_counter}: {exe_path}\n")
                    exe_counter += 1
            else:
                file.write("  No .exe files found\n")
            file.write("\n")

print(f"Executable file paths have been written to {exe_list_file}")





## ----------------- This will generate binary executable file of whole testsuits ----------------- ##

# Define the path to the testsuites directory
testsuites_path = os.path.abspath('build/riscv/beaglevfire/testsuites')

# Define the output file for directory names
directory_file = 'directory_names.txt'
# Define the output file for executable file paths
exe_list_file = 'exe_paths.txt'

# Get directory names
directories = []
with open(directory_file, 'r') as file:
    directories = [line.strip() for line in file]

# Open the output file for executable file paths in write mode
with open(exe_list_file, 'w') as file:
    exe_counter = 1  # Initialize a counter for numbering executables
    # Iterate through each directory name
    for directory in directories:
        dir_path = os.path.join(testsuites_path, directory)
        if os.path.isdir(dir_path):
            # Write the directory name to the file
            file.write(f"Directory: {dir_path}\n")
            # List the .exe files in the directory
            exe_files = [item for item in os.listdir(dir_path) if item.endswith('.exe')]
            if exe_files:
                # Write the full path of each .exe file with a unique number
                for exe_file in exe_files:
                    exe_path = os.path.abspath(os.path.join(dir_path, exe_file))
                    file.write(f"{exe_counter}: {exe_path}\n")
                    exe_counter += 1
            else:
                file.write("  No .exe files found\n")
            file.write("\n")

print(f"Executable file paths have been written to {exe_list_file}")


def generate_bin_from_exe(exe_path, elf_path, hss_yaml_content, hss_payload_gen_dir, payload_output):
    print(f"Processing: {exe_path}")
    
    if not os.path.isfile(exe_path):
        print(f"Error: {exe_path} does not exist. Skipping...")
        return

    # Convert .exe to .elf
    convert_command = f"riscv-rtems6-objcopy {exe_path} {elf_path}"
    conversion_status = os.system(convert_command)
    if conversion_status != 0:
        print(f"Error: Failed to convert {exe_path} to {elf_path}. Skipping...")
        return

    # Copy .elf to hss-payload-generator directory
    elf_dest_path = os.path.join(hss_payload_gen_dir, "test", os.path.basename(elf_path))
    try:
        shutil.copyfile(elf_path, elf_dest_path)
    except FileNotFoundError as e:
        print(f"Error: {e}. Skipping...")
        return
    except Exception as e:
        print(f"Unexpected error: {e}. Skipping...")
        return

    # Edit hss.yaml file
    yaml_path = os.path.join(hss_payload_gen_dir, "test/hss.yaml")
    try:
        with open(yaml_path, "w") as file:
            file.write(hss_yaml_content)
    except Exception as e:
        print(f"Error: Failed to edit {yaml_path}. {e}")
        return

    # Generate payload
    os.chdir(hss_payload_gen_dir)
    generate_payload_command = f"./hss-payload-generator -c test/hss.yaml {payload_output}"
    payload_status = os.system(generate_payload_command)
    if payload_status != 0:
        print(f"Error: Failed to generate {payload_output}. Skipping...")
        return

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

# Define paths
hss_payload_gen_dir = os.path.abspath("hart-software-services/tools/hss-payload-generator")
output_bins_dir = os.path.abspath("output_bins")
testsuites_dir = os.path.join(output_bins_dir, "testsuites")
os.makedirs(testsuites_dir, exist_ok=True)

# Read .exe paths from exe_paths.txt
exe_paths_file = os.path.abspath('exe_paths.txt')
exe_paths = []
current_dir = None

with open(exe_paths_file, 'r') as file:
    for line in file:
        if line.startswith('Directory:'):
            # Extract the directory path
            current_dir = line.strip().split('Directory: ')[1]
            # Create the directory structure under testsuites
            ensure_dir_exists(os.path.join(testsuites_dir, os.path.relpath(current_dir, start='/home/suraj02/quick-start/src/rtems/build/riscv/beaglevfire/testsuites')))
        elif line.strip() and line[0].isdigit():
            parts = line.strip().split(': ', 1)
            if len(parts) == 2:
                exe_paths.append((parts[1], current_dir))
            else:
                print(f"Skipping line due to unexpected format: {line}")

# Process each .exe file
for exe_counter, (exe_path, current_dir) in enumerate(exe_paths, 1):
    exe_path = os.path.abspath(exe_path)
    elf_path = exe_path.replace('.exe', '.elf')
    
    # Determine the output directory based on the current_dir
    rel_dir = os.path.relpath(current_dir, start='/home/suraj02/quick-start/src/rtems/build/riscv/beaglevfire/testsuites')
    target_dir = os.path.join(testsuites_dir, rel_dir)
    payload_output = os.path.join(target_dir, f"{os.path.basename(elf_path).replace('.elf', '.bin')}")
    
    hss_yaml_content = f"""set-name: 'PolarFire-SoC-HSS::RTEMS'
hart-entry-points: {{u54_1: '0x1000000000'}}
payloads:
  test/{os.path.basename(elf_path)}: {{exec-addr: '0x1000000000', owner-hart: u54_1, priv-mode: prv_m, skip-opensbi: true}}
"""
    generate_bin_from_exe(exe_path, elf_path, hss_yaml_content, hss_payload_gen_dir, payload_output)

print(f"All .bin files have been generated and stored in their respective directories under {testsuites_dir}")


