## Author: charley@edgeq.io
## Module: Programming nor-flash

import os
import subprocess
import sys
import struct

SECTOR_BLOCK_SIZE = 4096
ERASE_BLOCK_SIZE = 4096
MTD0_SIZE = 512
MTD1_SIZE = 128
MTD2_SIZE = 128
MTD3_SIZE = 5376
MTD4_SIZE = 2048

def action_function(nor_partition_dev_path, action_name, update_file, block_num):
    sector_block_size = 4096
    print(f"action for the commands: {nor_partition_dev_path}, {action_name}, {update_file}, {block_num}")
    if os.path.exists(nor_partition_dev_path):
        if action_name == "erase":
            print(f"Starting to erase {nor_partition_dev_path}")
            subprocess.run(["sudo", "flash_erase", nor_partition_dev_path, "0", block_num])
            print(f"Complete erasing partition {nor_partition_dev_path} zone")
        elif action_name == "update":
            if update_file:
                fixed_size = int(block_num) * sector_block_size
                input_size = int(os.path.getsize(update_file))
                if fixed_size >= input_size:
                    print(f"Starting to update {update_file} to {nor_partition_dev_path}")
                    subprocess.run(["sudo", "flashcp", "-v", update_file, nor_partition_dev_path])
                    print(f"Complete updating {update_file} to partition {nor_partition_dev_path}")
                else:
                    print(f"The update file size: {input_size} is larger than the current section size: {fixed_size}")
                    print(f"The update file: {update_file} cannot be written.")
            else:
                print("The written file is not input as the third parameter")
        elif action_name == "read":
            print(f"Start to read /dev/{nor_partition_dev_path} to {update_file}")
            subprocess.run(["sudo", "dd", "if=" + nor_partition_dev_path, "of=" + update_file])
            print(f"Complete the reading partition {nor_partition_dev_path} zone")
        elif action_name == "compare":
            if not update_file:
                print("The verified file is not input as the third parameter")
                return

            print(f"Starting to compare {nor_partition_dev_path} by using {update_file}")
            file1 = "/tmp/current_image.img"
            # Fixed size file to be written
            file2 = "/tmp/generat_image.img"
            subprocess.run(["sudo", "dd", f"if={nor_partition_dev_path}", f"of={file1}"])

            # Determine the size of the data zone
            FIXED_SIZE = int(block_num) * SECTOR_BLOCK_SIZE
            # Determine the size of the update file
            INPUT_SIZE = int(os.path.getsize(update_file))

            # print(f"The current update file size: {INPUT_SIZE}, and fixed size: {FIXED_SIZE}")
            if FIXED_SIZE >= INPUT_SIZE:
                subprocess.run(["sudo", "cp", f"{update_file}", f"{file2}"])
                # Copy the update file to the output file
                pad_size = FIXED_SIZE - INPUT_SIZE
                #subprocess.run(["sudo", "dd", "if=/dev/zero", "bs=1", "count=" + str(pad_size), "status=none", ">>", file2])

                if pad_size > 0:
                    with open(file2, 'ab') as f:
                        chunk_size = 1024 * 10 # 1MB chunks
                        while pad_size > chunk_size:
                            f.write(b'\377' * chunk_size)
                            if pad_size > chunk_size:
                                pad_size = pad_size - chunk_size
                            if pad_size <= chunk_size:
                                f.write(b'\377' * pad_size)
                                pad_size = 0
                        
                if subprocess.call(["cmp", "-s", file1, file2]) == 0:
                    print(f"The data in {nor_partition_dev_path} zone is the same as {update_file}'s contents.")
                else:
                    print(f"The data in {nor_partition_dev_path} zone is different from {update_file}'s contents.")
            else:
                print(f"The update file size: {INPUT_SIZE} is larger than the current section size: {FIXED_SIZE}")
                print("Cannot be compared for the current file.")
        elif action_name == "update-verify":
            FIXED_SIZE = int(block_num) * SECTOR_BLOCK_SIZE
            INPUT_SIZE = int(os.stat(update_file).st_size)
            if FIXED_SIZE >= INPUT_SIZE:
                print(f"Starting to update {update_file} to {nor_partition_dev_path}")
                subprocess.run(["sudo", "flashcp", "-v", update_file, nor_partition_dev_path])    
                # echo "Complete updating $update_file to partition $nor_partition_dev_path";
                # echo "Starting to verify $nor_partition_dev_path by using $update_file";
                file1 = "/tmp/current_image.img"
                # Fixed size file to be written
                file2 = "/tmp/generat_image.img"
                subprocess.run(["sudo", "dd", f"if={nor_partition_dev_path}", f"of={file1}"])

                subprocess.run(["sudo", "cp", f"{update_file}", f"{file2}"])
                # Copy the update file to the output file
                pad_size = FIXED_SIZE - INPUT_SIZE

                if pad_size > 0:
                    with open(file2, 'ab') as f:
                        chunk_size = 1024 * 10 # 1MB chunks
                        while pad_size > chunk_size:
                            f.write(b'\377' * chunk_size)
                            if pad_size > chunk_size:
                                pad_size = pad_size - chunk_size
                            if pad_size <= chunk_size:
                                f.write(b'\377' * pad_size)
                                pad_size = 0

                # Write the input file contents and filler characters to the output file
                if subprocess.call(["cmp", "-s", file1, file2]) == 0:
                    print(f"The data in {nor_partition_dev_path} zone is same as {update_file}'s contents")
                else:
                    print(f"The data in {nor_partition_dev_path} zone is different from {update_file}'s contents")
                # echo "Complete update-verify partition $nor_partition_dev_path zone by using $update_file";
            else:
                print(f"The update file size: {INPUT_SIZE} is larger than the current section size: {FIXED_SIZE}")
                print(f"The update file: {update_file} cannot be updated and verified.")
        else:
            print(f"Invalid action for partition {nor_partition_dev_path} zone")
    else:
        print("The partition or file does not exist.")


import sys

# Argument 5 is version number A0/B0
help_string = "help"
version_string = sys.argv[5]
filename = "/proc/device-tree/chip-version"
chip_version = ""

# read chip version from file
# with open(filename, "r") as f:
#    chip_version = f.read().strip()

if sys.argv[1] == help_string:
    print("command line: sudo ./program_nor_flash.py {partition name} {erase|update|compare/update-verify} {file name} {block number} {type: A0/B0}")
else:
    partition = sys.argv[1]
    if partition in ["mtd0", "mtd1", "mtd2", "mtd3", "mtd4", "mtd5", "mtd6", "mtd7", "mtd8", "mtd9"]:
        dev_file_path = "/dev/" + partition
        if len(sys.argv) > 3 and len(sys.argv) > 4:
            action_function(dev_file_path, sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Missing either update file or block size")
    else:
        print("Invalid partition or partition does not exist!!")
 





