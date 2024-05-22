# -*- coding: utf-8 -*-
"""
Created on Thu June 29 17:28:35 2023

@author: charley.lin@edgeq.io
"""

'''
Based on the download manifest.xml to install all downloaded files to
emmc partitioins, nor-flash A/B partition, and OTA scripts folder under ota partition
'''
import xml.etree.ElementTree as ET
import subprocess
import re
import argparse
import os
import tarfile
import shutil
import sys

default_contents_file_name='contents.xml'
default_partition_file_name='partition.xml'
default_manifest_file_name='manifest.xml'
default_emmc_blk='/dev/mmcblk0'
working_directory='/mnt/dist/'
partition_a_mtd='/dev/mtd6'
partition_b_mtd='/dev/mtd8'
CHIP_TYPE_B0='B0'


''' Below class install sparse files to emmc partitions and firmware to nor-flash'''

class emmc_install:
    def __init__(self, manifest_xml, source_path, ab_partition, chip_type):
        self.manifest_xml = manifest_xml
        self.source_path = source_path
        self.ab_partition = ab_partition
        self.chip_type = chip_type
    
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

    def find_partitions_for_files(self, xml_file, file_dir):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        file_partitions = {}

        for image in root.findall('.//image'):
            image_name = image.attrib['image_name']
            label1 = image.attrib.get('label1')
            label2 = image.attrib.get('label2')

            file_path = os.path.join(file_dir, image_name)
            if os.path.isfile(file_path):
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

    def has_pattern(self, string):
        pattern = r'\w+\.ext3'
        match = re.match(pattern, string)
        return bool(match)

    def is_norflash_needed(self, xml_file, image_name):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        nor_flash_dev='nor_flash'
        return_result=False
        firmware_install=root.find('.//firmware_install').text

        for image in root.findall('.//image'):
            find_image_name = image.attrib.get('image_name')
            dev_type = image.attrib.get('dev_type')
            if (find_image_name == image_name) and (dev_type == nor_flash_dev) and (firmware_install == 'yes'):
               return_result = True
               break
        return return_result
        

    def program_norflash(self, image_name, file_dir, ab_partition, chip_type):
        image_name_path=file_dir+'/'+image_name

        if chip_type == CHIP_TYPE_B0:
            if (ab_partition == 'a_partition'):
                print("Programing "+image_name+" to A partition in nor-flash")
                command = ["sudo", "flashcp", "-v", image_name_path, partition_a_mtd]
            elif (ab_partition == 'b_partition'):
                print("Programing "+image_name+" to B partition in nor-flash")
                command = ["sudo", "flashcp", "-v", image_name_path, partition_b_mtd]
            else:
                print("Not supported yet")
                sys.exit(633)
        else:
            print("Not supported yet")
            sys.exit(633)
             
        return_result=subprocess.call(command)
        # print(command)
        # return_result = 0
        return return_result
    
    def copy_files_by_extension(self, source_folder, destination_folder, extension):
        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        for file_name in os.listdir(source_folder):
            if file_name.endswith(extension):
                source_path = os.path.join(source_folder, file_name)
                destination_path = os.path.join(destination_folder, file_name)
                shutil.copy2(source_path, destination_path)
                # print(f"Copied file: {file_name}")

    def check_and_copy_tools(self, xml_file, source_folder):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        tools_source_folder=source_folder
        tools_destination_folder="./new_download"

        tools_install=root.find('.//tools_install').text
        if (tools_install == 'yes'):
            self.copy_files_by_extension(tools_source_folder, tools_destination_folder, ".sh")
            self.copy_files_by_extension(tools_source_folder, tools_destination_folder, ".py")
            self.copy_files_by_extension(tools_source_folder, tools_destination_folder, ".pem")


    def image_install(self, xml_file, file_dir, ab_partition, chip_type):
        dev_module="/dev/"
        file_partitions = self.find_partitions_for_files(xml_file, file_dir)
        return_result=0

        for image_name, partition_module in file_partitions.items():
            if len(partition_module) !=0 :
                if len(partition_module) == 1:
                    print("partition copy: "+image_name+" to "+partition_module[0])
                    command=["sudo", "dd", "if={0}".format(working_directory+image_name),"of={0}".format(dev_module+partition_module[0])]
                elif len(partition_module) == 2:
                    if ab_partition == 'a_partition':
                        print("partition copy: "+image_name+" to "+partition_module[0])
                        command=["sudo", "dd", "if={0}".format(working_directory+image_name),"of={0}".format(dev_module+partition_module[0])]
                    elif ab_partition == 'b_partition':
                        print("partition copy: "+image_name+" to "+partition_module[1])
                        command=["sudo", "dd", "if={0}".format(working_directory+image_name),"of={0}".format(dev_module+partition_module[1])]
                return_result=subprocess.call(command)
            else:
                '''
                   check the image_name is if for nor-flash or other device
                '''
                if self.is_norflash_needed(xml_file, image_name):
                    return_result=self.program_norflash(image_name, file_dir, ab_partition, chip_type)
                else:    
                    print("The image: "+image_name+" has no matched emmc partitions")

        # check and install all tools to the current rootfs
        self.check_and_copy_tools(xml_file,file_dir)

        return return_result

    def generate_installation_file(self, xml_file, output_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        partition_switch = root.find('partition_switch')
        if partition_switch is not None and partition_switch.text in ['yes', 'no']:
            partition_switch_value = partition_switch.text
            if partition_switch_value == 'yes':
                message = "partitionSwitch_upgrade: yes\n"
            else:
                message = "partitionSwitch_upgrade: no\n"
            
            with open(output_file, 'w') as file:
                file.write(message)

            print(f"Successfully generated the installation file '{output_file}'")
        else:
            print("Invalid value for 'partition_switch' field in the XML file.")
               
"""
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
                                         MAIN FUNCTIONS STARTS BELOW
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
"""
if __name__ == "__main__":
    print("Start to install all files to emmc and nor-flash!!")
	
    parser = argparse.ArgumentParser(description='''Install Files!''')
    parser.add_argument('--operator', type=str, default="", action="store", dest='operator', help='Enter the operator {build_self | build_third_party}')
    parser.add_argument('--manifest_xml', type=str, default="contents.xml", action="store", dest='manifest_xml', help='Enter the manifest.xml file')
    parser.add_argument('--source_path', type=str, default="", action="store", dest='source_path', help='Enter the source path for build sparse')
    parser.add_argument('--new_partition', type=str, default="", action="store", dest='new_partition', help='Enter new partition A/B')
    parser.add_argument('--chip_type', type=str, default="", action="store", dest='chip_type', help='Enter chip type {A0 | B0}')

    args=parser.parse_args()
    # print("The current arguments:"+args.manifest_xml+","+args.source_path+","+args.new_partition+','+args.chip_type)
    emmc_installer = emmc_install(args.manifest_xml, args.source_path, args.new_partition, args.chip_type)
    if args.operator == "install_emmc_op":
        emmc_installer.image_install(args.manifest_xml, args.source_path, args.new_partition, args.chip_type)
        emmc_installer.generate_installation_file(args.manifest_xml, "new_installation.txt")
    elif args.operator == "install_scripts":
        None
        # parse.build_thirdparty_files(args.build_ota_config, args.target_path, args.original_root)
    else:
        print("Wrong operator, please enter { install_emmc_op }")
        sys.exit(631)
    sys.exit(0)
