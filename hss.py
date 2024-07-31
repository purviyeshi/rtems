# This python script generates a single binary file from single executive file

import os
import shutil

# Define paths
exe_path = "build/riscv/beaglevfire/testsuites/samples/hello.exe"
elf_path = "build/riscv/beaglevfire/testsuites/samples/hello.elf"
hss_payload_gen_dir = "hart-software-services/tools/hss-payload-generator"
yaml_file = os.path.join(hss_payload_gen_dir, "test/hss.yaml")
elf_dest_path = os.path.join(hss_payload_gen_dir, "test/hello.elf")
payload_output = "hello.bin"

# Convert .exe to .elf
convert_command = f"riscv-rtems6-objcopy {exe_path} {elf_path}"
os.system(convert_command)
print(f"Converted {exe_path} to {elf_path}")

# Copy .elf to hss-payload-generator directory
shutil.copyfile(elf_path, elf_dest_path)
print(f"Copied {elf_path} to {elf_dest_path}")

# Edit hss.yaml file
hss_yaml_content = """set-name: 'PolarFire-SoC-HSS::RTEMS'
hart-entry-points: {u54_1: '0x1000000000'}
payloads:
  test/hello.elf: {exec-addr: '0x1000000000', owner-hart: u54_1, priv-mode: prv_m, skip-opensbi: true}
"""

with open(yaml_file, "w") as file:
    file.write(hss_yaml_content)
print(f"Edited {yaml_file} with hello.elf")

# Step 4: Generate payload
os.chdir(hss_payload_gen_dir)
generate_payload_command = f"./hss-payload-generator -c test/hss.yaml {payload_output}"
os.system(generate_payload_command)
print(f"Generated {payload_output}")













