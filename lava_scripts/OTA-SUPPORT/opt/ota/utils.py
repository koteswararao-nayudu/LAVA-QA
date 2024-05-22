## Author: charley@edgeq.io
## Module: All ultilities for upgrading

import xml.etree.ElementTree as ET
import subprocess
import argparse
import os
import sys
import binascii
import zlib
import struct
import datetime
import shutil
import glob
import re

# Example usage
# binary_data = b"This is a sample binary data that contains the pattern mmc 0:2, mmc 0:2"
mmc_a_partition = b"mmc 0:1"
mmc_b_partition = b"mmc 0:2"
mmc_temp_partition = b"mmc 0:9"
mmc_rootfs_a=b"mmcblk0p13"
mmc_rootfs_b=b"mmcblk0p14"
mmc_ota="/dev/mmcblk0p15"
check_filename = "./new_installation.txt"
version_filename = "/proc/device-tree/chip-version"
default_emmc_blk='/dev/mmcblk0'
install_package_file="/logdump/install_packge_file"

failsafe_partition="1"
a_partition="2"
b_partition="3"

# Define the structure format
# STRUCT_FORMAT = '<IILLQLLQL'  # Assumes little-endian byte order (for ARM64)
STRUCT_FORMAT = '<IiIIIIIII'  # Assumes little-endian byte order (for ARM64)
CRC_SIZE = 4
DATA_SIZE = 0x40000

#Nor-flash layout addresses mapping
b0_part_a_offset=0x00080000
b0_part_a_size=0x00400000
b0_part_failedsafe_offset=0x0080000
b0_part_failedsafe_size=0x00400000
b0_part_b_offset=0x01800000
b0_part_b_size=0x00400000


# It first converts the binary_data to a string using the decode() method with the errors argument set to 'replace', 
# which replaces any decoding errors with the Unicode replacement character U+FFFD. 
# Then it replaces the old_pattern with the new_pattern in the text using the replace() method. Finally, it converts the text back to binary data using the encode() method, and returns the result. The example usage shows how to use the function to replace the pattern "mmc 0:2" with "mmc 0:1" in a sample binary data.
''' Below class include the read/write nor flash file, replace a/b partition from the environment data'''
class upgrade_utility:
    def __init__(self, environment_path, new_partition, check_install, check_upgrade,
                 ota_store, mbr_data, ota_file,tar_folder, firmware_tar_file, fstab_file, manifest_xml, installed_ota_folder, 
                 show_curr_backup, current_env):
        self.environment_path = environment_path
        self.new_partition = new_partition
        self.check_install = check_install
        self.check_upgrade = check_upgrade
        self.ota_store= ota_store
        self.mbr_data = mbr_data
        self.ota_file = ota_file
        self.tar_folder = tar_folder
        self.firmware_tar_file = firmware_tar_file
        self.fstab_file = fstab_file
        self.manifest_xml = manifest_xml
        self.installed_ota_folder = installed_ota_folder
        self.show_curr_backup = show_curr_backup
        self.current_env = current_env
    
    def read_binary_data(self,nor_flash_file_path):
        with open(nor_flash_file_path, "rb") as f:
            binary_data = f.read()
        # print("Read nor flash data from the file: "+nor_flash_file_path)
        return binary_data

    def write_binary_data(self, nor_flash_file_path, binary_data):
        with open(nor_flash_file_path, "wb") as f:
            f.seek(0)
            f.write(binary_data)
        # print("Write binary data to the file: "+nor_flash_file_path)

    def replace_pattern(self, binary_data, old_pattern, new_pattern):
        # Convert the binary data to a string
        # text = binary_data.decode('utf-8', errors='ignore')
        # text = binary_data
        # Find all occurrences of the old patterns in the first part of the binary data
        data_part1 = binary_data[:DATA_SIZE]
        old_pattern_indexes_1 = [index for index in range(len(data_part1) - len(mmc_a_partition) + 1) if data_part1[index:index + len(mmc_a_partition)] == mmc_a_partition]
        old_pattern_indexes_2 = [index for index in range(len(data_part1) - len(mmc_b_partition) + 1) if data_part1[index:index + len(mmc_b_partition)] == mmc_b_partition]

        # Replace the old patterns with the new patterns
        if len(old_pattern_indexes_2) > 0:
            data_part1 = data_part1.replace(mmc_b_partition, mmc_a_partition)
            flag = 1
        elif len(old_pattern_indexes_1) > 0:
            data_part1 = data_part1.replace(mmc_a_partition, mmc_b_partition)
            flag = 2
        else:
            print("No partition flags found")
        
        # Recalculate the CRC checksum for the modified first part of the binary data
        crc = binascii.crc32(data_part1[CRC_SIZE:]) & 0xffffffff
        crc_bytes = crc.to_bytes(CRC_SIZE, 'little')

        # Write the new CRC checksum to the beginning of the modified first part of the binary data
        data_part1 = crc_bytes + data_part1[CRC_SIZE:]

        # Combine the modified first part of the binary data with the remaining unmodified part of the binary data
        text = data_part1 + binary_data[DATA_SIZE:]

        # Convert the text back to binary data
        # binary_data = text.encode('utf-8')
        binary_data = text

        return binary_data, flag

    def check_path_exists(self,path):
        if os.path.exists(path):
            if os.path.isfile(path):
                None
                # print(f"{path} has been found")
            elif os.path.isdir(path):
                print(f"{path} is a directory, no file exists")
                sys.exit("Exiting program")
            else:
                 print (path+" is not found")
                 sys.exit("Exiting program")
        else:
            print(f"{path} does not exist")
            sys.exit("Exiting program")
   
    def replacing(self):

        # check the path and file existing
        self.check_path_exists(self.environment_path)
        # read the nor flash environment to env_data
        env_data=self.read_binary_data(self.environment_path)
        new_env_data=""
        '''
        We are copying the tftp data on /tmp.
        This is a design decision and needs script changes in order to deployment
        '''
        if self.new_partition =="":
            new_env_data, flag=self.replace_pattern(env_data, "", "")
        elif self.new_partition == "a_partition":
                # print("Change nor flash environment to switch the partition A from B")
                new_env_data, flag=self.replace_pattern(env_data, mmc_b_partition, mmc_a_partition)
        elif self.new_partition == "b_partition":
                # print("Change nor flash environment to switch the partition B from A")
                new_env_data, flag=self.replace_pattern(env_data, mmc_a_partition, mmc_b_partition)
        else:
                print("Cannot support the partition input"+self.new_partition+" Please select {a_partition or b_partition}")
                sys._ExitCode(0)
        if (env_data != new_env_data):
            # print("Write new environment data to temp file")
            self.write_binary_data(self.environment_path,new_env_data)
        sys.exit(flag)
        
    def check_installation(self):
        # print ("self.check_install: "+self.check_install)
        # print ("self.check_upgrade: "+self.check_upgrade)
        # print ("filename: "+check_filename)
        try:
            with open(check_filename, "r") as f:
                
                for line in f:
                    # print(line)
                    line = line.strip() # remove whitespace characters
                    key, value = line.split(":") # split the line into two parts
                    if (self.check_install !="" and self.check_install in line.split(':')[0]):
                        # print ("key : "+key+" value: "+value)
                        if value.strip() == 'yes':
                            print("check result: yes")
                            sys.exit(1)
                        else:
                            print("check result: no")
                            sys.exit(0)
                    if (self.check_upgrade !="" and self.check_upgrade in line.split(':')[0]):
                        if value.strip() == 'yes':
                            print("check result: yes")
                            sys.exit(1)
                        else:
                            print("check result: no")
                            sys.exit(0)
        except FileNotFoundError:
            print(f"Error: File '{check_filename}' not found.")
            sys.exit(1)
        except IOError:
            print(f"Error: Unable to read from file '{check_filename}'.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

        sys.exit(0)

    def print_mbr(self, header, partition_selection, flag, partition_failedsafe_offset, partition_failedsafe_size,
                  partition_a_offset, partition_a_size, partition_b_offset, partition_b_size):
            print('Header:', hex(header))
            print('Partition Selection:', hex(partition_selection))
            print('Flag:', hex(flag))
            print('Partition Failedsafe Offset:', hex(partition_failedsafe_offset))
            print('Partition Failedsafe Size:', hex(partition_failedsafe_size))
            print('Partition A Offset:', hex(partition_a_offset))
            print('Partition A Size:', hex(partition_a_size))
            print('Partition B Offset:', hex(partition_b_offset))
            print('Partition B Size:', hex(partition_b_size))
         

    def change_mbr_file(self, env_data, prefer_partition):

        # Unpack the binary data into the structure
        header, partition_selection, flag, partition_failedsafe_offset, partition_failedsafe_size, partition_a_offset, partition_a_size, partition_b_offset, partition_b_size = struct.unpack(STRUCT_FORMAT, env_data[:36])

        # Check if the header matches the expected value
        if header != 0xAA55AA55:
            print('Header:', hex(header))
            print('Error: Invalid header in binary file')
            sys.exit(0)
        else:
            # self.print_mbr(header, partition_selection, flag, partition_failedsafe_offset, partition_failedsafe_size,
            #      partition_a_offset, partition_a_size, partition_b_offset, partition_b_size)
            None
        if prefer_partition =="":
            if (partition_selection==2):
                partition_selection = 3
            elif (partition_selection==3):
                partition_selection = 2
            else:
                partition_selection = 1
        elif prefer_partition == a_partition:
            # print("Change nor flash environment to switch the partition A from B")
            partition_selection = 2
        elif prefer_partition == b_partition:
            # print("Change nor flash environment to switch the partition B from A")
            partition_selection = 3
        elif prefer_partition == failsafe_partition:
            partition_selection = 1
        else:
            partition_selection = 2
        # print("The current partition selection:", partition_selection)

        if (hex(partition_failedsafe_offset) != b0_part_failedsafe_offset):
               partition_failedsafe_offset= b0_part_failedsafe_offset 
        if (hex(partition_failedsafe_size) != b0_part_failedsafe_size):
               partition_failedsafe_size= b0_part_failedsafe_size
        if (hex(partition_b_offset) != b0_part_b_offset):
               partition_b_offset= b0_part_b_offset
        if (hex(partition_b_size) != b0_part_b_size):
               partition_b_size= b0_part_b_size
        # print("New MBR sector data:")
        # self.print_mbr(header, partition_selection, flag, partition_failedsafe_offset, partition_failedsafe_size,
        #          partition_a_offset, partition_a_size, partition_b_offset, partition_b_size)

    
         # Pack the updated structure into binary data
        updated_data = struct.pack(STRUCT_FORMAT, header, partition_selection, flag, partition_failedsafe_offset, partition_failedsafe_size, partition_a_offset, partition_a_size, partition_b_offset, partition_b_size)

        # Write the updated binary data back to the file
        with open(self.mbr_data, 'r+b') as file:
            file.write(updated_data)

        # print('Updated partition selection:', partition_selection)
        # print('Binary file data updated successfully.')
        return partition_selection-1

    def check_partition(self):
        flag=0
        # check the path and file existing
        self.check_path_exists(self.mbr_data)
        # read the nor flash environment to env_data
        env_data=self.read_binary_data(self.mbr_data)
        new_env_data=""

        if self.new_partition =="":
            flag=self.change_mbr_file(env_data, "")
        elif self.new_partition == "a_partition":
                # print("Change nor flash environment to switch the partition A from B")
                flag=self.change_mbr_file(env_data, a_partition)
        elif self.new_partition == "b_partition":
                # print("Change nor flash environment to switch the partition B from A")
                flag=self.change_mbr_file(env_data, b_partition)
        elif self.new_partition == "failsafe_partition":
                # print("Change nor flash environment to switch the partition B from A")
                flag=self.change_mbr_file(env_data, failsafe_partition)
        else:
                print("Cannot support the partition input"+self.new_partition+" Please select {a_partition or b_partition}")
                sys._ExitCode(0)

        #if (env_data != new_env_data):
            # print("Write new environment data to temp file")
        #    self.write_binary_data(self.environment_path,new_env_data)
        sys.exit(flag)

    def store_ota_package(self):
        # read the product information from the XML file
        # Path to the pre-defined folder
        mnt_path = '/mnt'
        if os.path.isfile(self.ota_store):
            tree = ET.parse(self.ota_store)
            root = tree.getroot()
            
            # get the current date/time
            now = datetime.datetime.now()

            # Format the date and time
            formatted_date_time = now.strftime('%m-%d-%Y-%H-%M-%S')

            # print("manifest signature: {}".format(root.find('signature').text))
            version = root.find('.//version').text
            product_name = root.find('product_name').text
            image_file_name = root.find('.//image_file_name').text
            new_dir_name_download="/mnt/"+"ota"+"-"+formatted_date_time+"-"+version+"-"+product_name+"-"+image_file_name
            mount_result=subprocess.call(["mount", "/dev/mmcblk0p15", "/mnt"])
            if mount_result != 0:
                 print("OTA partition error!!")
                 sys.exit(620)
            # Get the size of the folder in bytes
            folder_size = int(shutil.disk_usage(mnt_path).total)
            used_folder_size = int(shutil.disk_usage(mnt_path).used)
            free_folder_size = int(shutil.disk_usage(mnt_path).free)
            download_file_size = int(os.path.getsize(self.ota_file))
            if ((folder_size - used_folder_size) > (download_file_size*2)):
                subprocess.call(["mkdir", "-p", new_dir_name_download])
                subprocess.call(["cp", self.ota_file, new_dir_name_download+"/"])
                subprocess.call(["cp", self.ota_store, new_dir_name_download+"/"])
            else:
                print("Warning: No space for downloading file to ota partition!!")
                print("The oldest downloaded package will be deleted!!")
                # Find the latest created folder inside the root folder
                folders = glob.glob(os.path.join(mnt_path, '*'))
                folders = [f for f in folders if os.path.isdir(f)]
                if folders and len(folders) > 0:
                    oldest_folder = min(folders, key=os.path.getctime)
                    print("The current oldest folder: "+oldest_folder)
                    subprocess.call(["rm", "-rf", oldest_folder])
                    subprocess.call(["mkdir", "-p", new_dir_name_download])
                    subprocess.call(["cp", self.ota_file, new_dir_name_download+"/"])
                    subprocess.call(["cp", self.ota_store, new_dir_name_download+"/"])                   
                else:
                    print("No folder is founded")
                    subprocess.call(["umount", "/mnt"])
                    sys.exit(0)                
            # subprocess.call(["umount", "/mnt"])
        else:
             print("Not find manifest.xml")
             return ""
    
    def show_ota(self):
        subprocess.call(["sudo", "mount", "/dev/mmcblk0p15", "/mnt"])
        print("The donwloaded ota packages list:")
        subprocess.call(["ls", "-lpt", "/mnt"])
        subprocess.call(["sudo", "umount", "/mnt"])
        print("Complete the ota package list")
    
    def replacing_b0(self):
        None

    def find_tar_files(self, folder):
        # Get the list of tar.gz files inside the specified folder
        # print(folder)
        tar_files = glob.glob(os.path.join(folder, '*.tar.gz'))
    
        if not tar_files:
            # print("No tar.gz files found.")
            subprocess.call(["umount", "/mnt"])
            sys.exit(0)
        else:
            # print("Find out the tar.gz file: "+ tar_files[0])
            # print(folder)
            # print(tar_files[0])
            return (folder + '\n' + tar_files[0])
    
    def clean_none_ota(self):
        directory = '/mnt'

        # Get a list of all subdirectories in the directory
        subdirectories = [entry for entry in os.listdir(directory) if os.path.isdir(os.path.join(directory, entry))]

        # Iterate over the subdirectories
        for subdir in subdirectories:
            # Check if the subdirectory name matches the desired patterns
            if subdir.startswith('ota-') or subdir == 'tools':
                continue  # Skip the subdirectory
            else:
                subdir_path = os.path.join(directory, subdir)
                # Remove the subdirectory and all its contents
                # print(f"Removing directory: {subdir_path}")
                shutil.rmtree(subdir_path)
  
    def find_out_tarfile(self):
        # Specify the root folder
        mnt_folder="/mnt"
        subprocess.call(["mount", "/dev/mmcblk0p15", mnt_folder])
        self.clean_none_ota()

        # Check if a folder name is provided as command line argument
        if self.tar_folder != "":
            input_folder = self.tar_folder
            folder_path = os.path.join(mnt_folder, input_folder)
            if not os.path.exists(folder_path):
                #print("Specified folder not found.")
                subprocess.call(["umount", "/mnt"])
                # print("Complete the ota package list")
                sys.exit(0)
            else:
                # print("Complete the ota package list")
                return self.find_tar_files(folder_path)
        else:
            # Find the latest created folder inside the root folder
            folders = glob.glob(os.path.join(mnt_folder, '*'))
            folders = [f for f in folders if os.path.isdir(f) and "ota-" in f]
            if folders and len(folders) > 0:
                latest_folder = max(folders, key=os.path.getctime)
            else:
                 subprocess.call(["umount", "/mnt"])
                 sys.exit(0)
            # print("Complete the ota package list")
            return self.find_tar_files(latest_folder)
    
    def copy_firmware(self, firmware_tar_file):
        target_file_name = "target.tar.gz"
        mnt_folder="/mnt"
        release_package_name="release_package"
        subprocess.call(["sudo", "tar", "-xzvf", firmware_tar_file, "-C", mnt_folder])

        # Variable to store the full path of the target file
        target_file_path = None

        # Recursively search for the "target.tar.gz" file within the "release_package" folder
        for root, dirs, files in os.walk(mnt_folder):
            if release_package_name in dirs:
                release_package_path = os.path.join(root, release_package_name)
                file_path = os.path.join(release_package_path, target_file_name)
                if os.path.exists(file_path):
                    target_file_path = file_path
                    break

        # Move the target file to the destination folder if found
        if target_file_path:
            destination_path = os.path.join(mnt_folder, target_file_name)
            shutil.move(target_file_path, destination_path)
            print("File moved successfully.")
        else:
            print("Target file not found in the 'release_package' folder.")
            sys.exit(640)

        # untar the target.tar.gz under /tmp
        subprocess.call(["sudo", "tar","-xzvf", target_file_name, "-C", mnt_folder])
        firmware_file="/mnt/FIRMWARE.sparse"
        if os.path.isfile(firmware_file):
            #  sudo mount -o loop ./FIRMWARE.sparse ./linux_test
            subprocess.call(["sudo", "mkdir", "-p", "/mnt/FIRMWARE"])
            subprocess.call(["sudo", "mount", "-o", "loop", "/mnt/FIRMWARE.sparse", "/mnt/FIRMWARE"])

            # copy /mnt/FIRMWARE/FIRMWARE.bin to /tmp/FIRMWARE
            subprocess.call(["sudo", "mkdir", "-p", "/tmp/FIRMWARE"])
            subprocess.call(["sudo", "cp", "/mnt/FIRMWARE/FIRMWARE.bin", "/tmp/FIRMWARE/"])

            # umount 
            subprocess.call(["sudo", "umount", "/mnt/FIRMWARE"])
        else:
            print("No FIRMWARE.sparse in this tar file: "+firmware_tar_file)
            sys.exit(640)

        # cleanup the /mnt
        # Get a list of all files directly under the mnt_folder
        files = [os.path.join(mnt_folder, f) for f in os.listdir(mnt_folder) if os.path.isfile(os.path.join(mnt_folder, f))]

        # Iterate over the files
        for file_path in files:
            # Remove the file
            os.remove(file_path)
            print(f"Removed file: {file_path}")             
        self.clean_none_ota()

    def workon_firmware_to_tmp(self):
        # Specify the root folder
        mnt_folder="/mnt"
        subprocess.call(["mount", "/dev/mmcblk0p15", mnt_folder])

        # Check if a folder name is provided as command line argument
        if self.firmware_tar_file != "":
            if not os.path.isfile(self.firmware_tar_file):
                print("The current tar file doesn't exists, "+self.firmware_tar_file)
                subprocess.call(["umount", "/mnt"])
                # print("Complete the ota package list")
                sys.exit(640)
            else:
                print("Untar the current tar ball and build FIRMWARE original file")
                return self.copy_firmware(self.firmware_tar_file)
        else:
            print("Cannot find the tar ball, tar is empty!!")
            subprocess.call(["umount", "/mnt"])
            sys.exit(640)

    def find_partition_by_label(self, label_name):
        command = ['lsblk', '-o', 'NAME,PARTLABEL', '-l', '-n', default_emmc_blk]
        output = subprocess.check_output(command, text=True).strip()

        for line in output.split('\n'):
            partition_info = line.split()
            if len(partition_info) >= 2:
                partition_name = partition_info[0]
                partition_label = partition_info[1]
                if partition_label == label_name:
                    return partition_name

        return None
    
    def find_partitions(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        file_partitions = {}

        for image in root.findall('.//image'):
            image_name = image.attrib['image_name']
            label1 = image.attrib.get('label1')
            label2 = image.attrib.get('label2')

            labels = []
            if label1:
                partition = self.find_partition_by_label(label1)
                if partition:
                    labels.append(partition)
            if label2:
                partition = self.find_partition_by_label(label2)
                if partition:
                    labels.append(partition)

                file_partitions[image_name] = labels

        # print("The current partition matching:")
        # print(file_partitions)
        return file_partitions
    '''
    def remove_lines_based_partition(self, xml_file, ab_partition):
        patterns = ['/logdump', '/coredump', '/ota']
        with open(xml_file, 'r') as file:
            lines = file.readlines()

        if ab_partition == 'a_partition':
            lines = self.process_odd_lines(lines, patterns)
        elif ab_partition == 'b_partition':
            lines = self.process_even_lines(lines, patterns)

        with open(xml_file, 'w') as file:
            file.writelines(lines)

    def process_odd_lines(self, lines, patterns):
        processed_lines = []
        for i, line in enumerate(lines):
            if i % 2 != 0 or any(pattern in line for pattern in patterns) or self.has_same_after_slash(line):
                processed_lines.append(line)
        return processed_lines

    def process_even_lines(self, lines, patterns):
        processed_lines = []
        for i, line in enumerate(lines):
            if i % 2 == 0 or any(pattern in line for pattern in patterns) or self.has_same_after_slash(line):
                processed_lines.append(line)
        return processed_lines

    def has_same_after_slash(self, line):
        match = re.search(r'/(?P<word>\w+)\s', line)
        if match:
            word = match.group('word')
            return line.count('/' + word) > 1
        return False
    '''

    def remove_lines_with_patterns(self, file_path, ab_partition):
        odd_patterns = ['/logdump', '/coredump', '/ota', '/data']
        even_patterns = ['/logdump', '/coredump', '/ota', '/data']
        with open(file_path, 'r') as file:
            lines = file.readlines()
        if (len(lines)-4) <= 5:
            print("fstab file was created")
            return

        # if ab_partition == 'a_partition':
        #     lines = [line for i, line in enumerate(lines) if i ==0 or i % 2 != 0 or any(pattern in line for pattern in odd_patterns)]
        # elif ab_partition == 'b_partition':
        #     lines = [line for i, line in enumerate(lines) if i % 2 == 0 or any(pattern in line for pattern in even_patterns)]

        new_lines=[]
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                # print("Current fstab the second parts:")
                if (ab_partition == 'a_partition' and (parts[1].split('_') is not None or parts[1] in odd_patterns)):
                    if parts[1] not in odd_patterns and len(parts[1].split('_'))>=2:
                        if parts[1].split('_')[len(parts[1].split('_'))-1] == 'a':
                            parts[1] = parts[1].split('_')[0]
                            modified_line = ' '.join(parts)
                            new_lines.append(modified_line + '\n')
                    elif parts[1] in odd_patterns:
                            modified_line = ' '.join(parts)
                            new_lines.append(modified_line + '\n')                 
                if (ab_partition == 'b_partition'):
                    if parts[1] not in odd_patterns and len(parts[1].split('_'))>=2:
                        if parts[1].split('_')[len(parts[1].split('_'))-1] == 'b':
                            parts[1] = parts[1].split('_')[0]
                            modified_line = ' '.join(parts)
                            new_lines.append(modified_line + '\n')
                    elif parts[1] in odd_patterns:
                            modified_line = ' '.join(parts)
                            new_lines.append(modified_line + '\n')               

        with open(file_path, 'w') as file:
            file.writelines(new_lines)



    def work_on_fstab(self, xml_file,fstab_file, ab_partition):
        mnt_folder="/mnt"
        dev_module="/dev/"
        file_partitions = self.find_partitions(xml_file)
        return_result=0

        self.remove_lines_with_patterns(fstab_file, ab_partition)
        
        for image_name, partition_module in file_partitions.items():
            if (image_name == "rootfs.ext3"):
                if len(partition_module) !=0 :
                    if len(partition_module) == 1:
                        print("Not copy the fstab to the new rootfs")
                    elif len(partition_module) == 2:
                        if ab_partition == 'a_partition':
                            print("copy the new fstab to "+partition_module[0])
                            command=["sudo", "mount", "{0}".format(dev_module+partition_module[0]), "/mnt"]
                        elif ab_partition == 'b_partition':
                            print("copy the new fstab to "+partition_module[1])
                            command=["sudo", "mount", "{0}".format(dev_module+partition_module[1]), "/mnt"]
                        return_result=subprocess.call(command)
                        subprocess.call(["sudo","cp","{0}".format(fstab_file), "/mnt/etc/"])

    def get_deepest_folder(self, full_path):
        # Normalize the path to handle different separators (e.g., / or \)
        normalized_path = os.path.normpath(full_path)

        # Get the deepest folder using basename
        deepest_folder = os.path.basename(normalized_path)

        return deepest_folder
    
    def install_ota_to_intermeduim(self):
        env_file=self.current_env
        # check the path and file existing
        self.check_path_exists(env_file)
        # read the nor flash environment to env_data
        env_data=self.read_binary_data(env_file)
        current_partition=self.get_current_partition(env_data)

        current_ota_name = self.get_deepest_folder(self.installed_ota_folder)

        try:
            with open(install_package_file, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"'{install_package_file}' not found.")
            subprocess.call(["sudo", "touch", install_package_file])
            lines=[]
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(638)

        try:
            with open(install_package_file, 'w') as file:
                found_partition = False
                for line in lines:
                    if current_partition == "a_partition" and line.startswith("a_partition:"):
                        line = "a_partition:" + current_ota_name + "\n"
                        found_partition = True
                    elif current_partition == "b_partition" and line.startswith("b_partition:"):
                        line = "b_partition:" + current_ota_name + "\n"
                        found_partition = True
                    file.write(line)
                # If the input partition was not found, add it as a new line
                if not found_partition:                
                    file.write(current_partition+":"+current_ota_name + '\n')

            # print(f"Line '{current_ota_name}' added to '{install_package_file}' successfully.")
        except Exception as e:
            print(f"Error occurred while adding line: {e}")
            sys.exit(638)

    def get_third_token_from_uname(self):
        try:
            # Run the "uname -a" command and capture its output
            uname_output = subprocess.check_output(["uname", "-a"]).decode().strip()

            # Split the output into tokens based on whitespace
            tokens = uname_output.split()

            # Check if there are at least three tokens
            if len(tokens) >= 3:
                # Get the third token (index 2)
                third_token = tokens[2]
                return third_token
            else:
                print("Error: Not enough tokens in the output of 'uname -a'.")
                return None
        except Exception as e:
            print(f"Error occurred while active 'uname -a': {e}")
            return None

    def get_current_partition(self, env_data):
        # Unpack the binary data into the structure
        header, partition_selection, flag, partition_failedsafe_offset, partition_failedsafe_size, partition_a_offset, partition_a_size, partition_b_offset, partition_b_size = struct.unpack(STRUCT_FORMAT, env_data[:36])
        return_partition=''

        # Check if the header matches the expected value
        if header != 0xAA55AA55:
            print('Header:', hex(header))
            print('Error: Invalid header in binary file')
            return return_partition
        else:
            # self.print_mbr(header, partition_selection, flag, partition_failedsafe_offset, partition_failedsafe_size,
            #      partition_a_offset, partition_a_size, partition_b_offset, partition_b_size)
            None
        if (partition_selection==2):
            # partition_selection = 3
            return_partition="a_partition"
        elif (partition_selection==3):
            # partition_selection = 2
            return_partition="b_partition"
        else:
            partition_selection = 1
            return_partition=""
        return return_partition
    
    def get_installed_ota_folder(self):
        a_partition_ota=""
        b_partition_ota=""
        try:
            with open(install_package_file, 'r') as file:
                for line in file:
                    if "a_partition:" in line:
                        a_partition_index = line.index("a_partition:")
                        a_partition_ota=line[a_partition_index + len("a_partition:") :].strip()
                        # print(f"Found '{backup_ota}' from '{line}'")
                    if "b_partition:" in line:
                        b_partition_index = line.index("b_partition:")
                        b_partition_ota=line[b_partition_index + len("b_partition:") :].strip()
                        # print(f"Found '{backup_ota}' from '{line}'")
                return a_partition_ota, b_partition_ota
        except Exception as e:
            # print(f"Error in '{install_package_file}': {e}")
            return a_partition_ota, b_partition_ota

    def print_partition_info(self, partition_path, partition_id, current_backup):
        #print("partition_path: "+partition_path)
        #print("partition_id: "+ partition_id)
        #print("current_backup: "+ current_backup)
        if partition_id == "a_partition" and current_backup == "current":
            print("The current active package is in partition A")
        if partition_id == "a_partition" and current_backup == "next":
            print("The standby package is in partition A")        
        if partition_id == "b_partition" and current_backup == "current":
            print("The current active package is in partition B")
        if partition_id == "b_partition" and current_backup == "next":
            print("The standby package is in partition B")

        current_manifest_xml=partition_path+"/manifest.xml"
        # print("current manifest.xml:"+current_manifest_xml)
        if not os.path.isfile(current_manifest_xml):
            print("XML doesn't exist: "+current_manifest_xml)
            sys.exit(645)
        tree = ET.parse(current_manifest_xml)
        root = tree.getroot()
        product_name = root.find('product_name').text
        version = root.find('.//version').text
        build_id = root.find('build_id').text
        board_name = root.find('.//board_name').text
        print("The package info in folder "+partition_path+":")
        print("Product name: "+ product_name)
        print("Build ID: "+ build_id)
        print("Version: "+ version)
        print("Board Info: "+ board_name)

    def display_curr_backup(self):
        env_file=self.show_curr_backup
        # check the path and file existing
        self.check_path_exists(env_file)
        # read the nor flash environment to env_data
        env_data=self.read_binary_data(env_file)

        current_version=self.get_third_token_from_uname()
        current_partition=self.get_current_partition(env_data)
        
        if current_partition=="":
            print("Not get the current partition from MBR!!")
            sys.exit(644)
        backup_partition=""
        if (current_partition == 'a_partition'):
            backup_partition='partition B'
            current_partition='partition A'
        elif (current_partition == 'b_partition'):
            backup_partition='partition A'
            current_partition='partition B'
        print("Current active package: "+current_version+" in "+current_partition)
        l1l2_version = subprocess.check_output(["cat", "/mgmt/etc/raptor2_software_version.txt"]).decode().strip()
        print("Current active L1, L2 version: "+l1l2_version)
        
        
        a_partition_ota, b_partition_ota=self.get_installed_ota_folder()
        a_partition_path="/ota/"+a_partition_ota
        b_partition_path="/ota/"+b_partition_ota
        # print("Current Partition: A, B: "+a_partition_ota+","+b_partition_ota)
        if not os.path.exists(a_partition_path) and not os.path.exists(b_partition_path):
            print("The partition A and partition B packages do not exist!!")
            sys.exit(645)
        else:
            #print("Backup package: "+self.get_installed_ota_folder()+" in "+backup_partition)
            # print("Next switched package in "+backup_partition)

            if os.path.exists(a_partition_path) and current_partition == "partition A" and not a_partition_ota == "":
                self.print_partition_info(a_partition_path, "a_partition", "current")
            else:
                if os.path.exists(a_partition_path) and not a_partition_ota == "":
                    self.print_partition_info(a_partition_path, "a_partition", "next")
   
            if os.path.exists(b_partition_path) and current_partition == "partition B" and not b_partition_ota == "":
                self.print_partition_info(b_partition_path, "b_partition", "current")
            else:
                if os.path.exists(b_partition_path) and not b_partition_ota == "":
                    self.print_partition_info(b_partition_path, "b_partition", "next")
    
    def mount_if_not_mounted(self, source, target):
        if not os.path.ismount(target):
            try:
                subprocess.run(["sudo", "mount", source, target], check=True)
                print(f"Successfully mounted {source} to {target}.")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while mounting: {e}")
        else:
            # print(f"{source} is already mounted to {target}.")
            None

if __name__ == "__main__":
    # print("Start to change environments in nor flash..!!")
	
    parser = argparse.ArgumentParser(description='''General ultility for system upgrade!''')
    parser.add_argument('--environment_path', type=str, default="", action="store", dest='environment_path', help='Enter file path and name for tempoary nor flash environment data')
    parser.add_argument('--new_partition', type=str, default="", action="store", dest='new_partition', help='Enter the location to emmc {a_partition|b_partition}')
    parser.add_argument('--check_install', type=str, default="", action="store", dest='check_install', help='Enter the which module to be installed (emmc, rootfs, tools, firmware)')
    parser.add_argument('--check_upgrade', type=str, default="", action="store", dest='check_upgrade', help='Enter the which module to be upgraded (partitionSwitch)')
    parser.add_argument('--ota_store', type=str, default="", action="store", dest='ota_store', help='Enter the manifest.xml path/file')
    parser.add_argument('--mbr_path', type=str, default="", action="store", dest='mbr_data', help='Enter file path and name for tempoary nor flash environment data')
    parser.add_argument('--show_ota', type=str, default="", action="store", dest='show_ota', help='No needed to enter any')
    parser.add_argument('--ota_file', type=str, default="", action="store", dest='ota_file', help='Enter the tar ball to be installed')
    parser.add_argument('--check_tar_file', type=str, default="", action="store", dest='check_tar_file', help='Check the tar ball from the folder')
    parser.add_argument('--tar_folder', type=str, default="", action="store", dest='tar_folder', help='Enter the folder which have tar.gz file')
    parser.add_argument('--get_firmware_bin', type=str, default="", action="store", dest='firmware_tar_file', help='Enter the tar file which contains the firmware.bin ')
    parser.add_argument('--fstab_file', type=str, default="", action="store", dest='fstab_file', help='Enter the fstab file ')
    parser.add_argument('--manifest_xml', type=str, default="", action="store", dest='manifest_xml', help='Enter the manifest.xml file ')
    parser.add_argument('--installed_ota_folder', type=str, default="", action="store", dest='installed_ota_folder', help='Enter the installed ota folder name')
    parser.add_argument('--show_curr_backup', type=str, default="", action="store", dest='show_curr_backup', help='Enter env data, show the current and backup packages')
    parser.add_argument('--current_env', type=str, default="", action="store", dest='current_env', help='Enter env data, for the store the ota package')
    
    args=parser.parse_args()
    # print("The current arguments:"+args.environment_path+","+args.mbr_data)
    chip_type = ''
    parse = upgrade_utility(args.environment_path, args.new_partition, args.check_install, args.check_upgrade, args.ota_store, args.mbr_data,
                            args.ota_file, args.tar_folder, args.firmware_tar_file, args.fstab_file, args.manifest_xml, args.installed_ota_folder,
                            args.show_curr_backup, args.current_env)
    if os.path.exists(version_filename):
        with open(version_filename, "r") as f:
            chip_type = f.read().strip()
    else:
        chip_type = 'A0'

    if (args.check_install != "" or args.check_upgrade != "" ):
        parse.check_installation()
    elif (args.environment_path != "" ):
        if ("A0" in chip_type):
            parse.replacing()
            print("Select A0")
        elif "B0" in chip_type:
            parse.replacing_b0()
            print("Select B0")
        else:
            print("Not supported yet.")
            #sys.exit(0)
    elif (args.mbr_data != ""):
            # print("Start to select the partition...")
            parse.check_partition()        
    elif (args.ota_store != "" and args.ota_file != ""):
         sys.exit(parse.store_ota_package())
    elif (args.show_ota != ""):
         sys.exit(parse.show_ota())
    elif (args.check_tar_file != ""):
         found_folder_and_file= parse.find_out_tarfile()
         subprocess.call(["umount", "/mnt"])
         print(found_folder_and_file)
         sys.exit(0)
    elif (args.firmware_tar_file != ""):
         cur_firmware_bin= parse.workon_firmware_to_tmp()
         subprocess.call(["umount", "/mnt"])
         sys.exit(0)
    elif (args.fstab_file != "" and args.manifest_xml != "" and args.new_partition != ""):
         parse.work_on_fstab(args.manifest_xml, args.fstab_file, args.new_partition)
         subprocess.call(["sudo", "umount", "/mnt"])
         sys.exit(0)
    elif (args.installed_ota_folder != "" and args.current_env != ""):
         source = "/dev/mmcblk0p11"
         target = "/logdump"
         parse.mount_if_not_mounted(source, target)
         parse.install_ota_to_intermeduim()
         sys.exit(0)
    elif (args.show_curr_backup != ""):
         source = "/dev/mmcblk0p11"
         target = "/logdump"
         parse.mount_if_not_mounted(source, target)
         parse.display_curr_backup()
         sys.exit(0)
    else:
         print("Not correct parameters")



