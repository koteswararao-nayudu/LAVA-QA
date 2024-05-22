import sys
import os

# Check if two command line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <string1>")
    sys.exit(1)

# Get input strings from command line arguments
filename = sys.argv[1]

if os.path.exists(filename):
    None
else:
    print("the file:"+filename+" doesn't exist!")
    sys.exit(1)

# Read the contents of the input file
with open(filename, 'r') as f:
    for line in f:
        # Extract string1 and string2 from the lines
        string1=line
        # print("current reading: "+line)
        # Extract the first part of string1 and write to 'rootfs_part_main.txt'
        if ('name="rootfs_a"' in string1 or 'name="rootfs"' in string1):
            part1 = string1.split(' :')[0].strip()
            with open('rootfs_part_main.txt', 'w') as f:
                f.write(part1)

        # Extract the first part of string2 and write to 'rootfs_part_backup.txt'
        if 'name="rootfs_b"' in string1:
            part1 = string1.split(':')[0].strip()
            with open('rootfs_part_backup.txt', 'w') as f:
                f.write(part1)