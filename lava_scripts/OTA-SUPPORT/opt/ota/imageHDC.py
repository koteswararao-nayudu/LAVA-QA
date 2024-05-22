# -*- coding: utf-8 -*-
"""
Created on Thu July 19, 2023, 17:28:35

@author: charley.lin@edgeq.io
"""

'''
This class will add a header for an image, and split a image header
'''
import xml.etree.ElementTree as ET
import subprocess
import re
import argparse
import os

import struct
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

class image_header:
    def __init__(self, input_image_file, output_image_file, image_type, auth_type, image_name):
        self.input_image_file = input_image_file
        self.output_image_file = output_image_file
        self.image_type = int(image_type)
        self.auth_type = int(auth_type)
        self.image_name = image_name
    
    def image_header_add(self):
        # check the file existing
        if not os.path.isfile(self.input_image_file):
            print("Input image doesn't exist!!")
            sys.exit(613)
        # Load the image
        with open(self.input_image_file, 'rb') as f:
            image_data = f.read()

        image_size = len(open(self.input_image_file, 'rb').read())

        # Create the header
        header_data = struct.pack('I', 0xAA55AA55)  # First 4 bytes: 0xAA55AA55
        header_data += struct.pack('I', self.image_type)  # Next 4 bytes: Image type (0: normal, 1: encrypted)
        header_data += struct.pack('I', image_size)  # Next 4 bytes: Image size
        header_data += struct.pack('I', self.auth_type)  # Next 4 bytes: Authentication type
        header_data += self.image_name.encode('utf-8').ljust(48, b'\x00')  # Last 48 bytes: Image file name

        # Combine header with image data
        final_data = header_data + image_data

        if os.path.isfile(self.output_image_file):
            subprocess.call(["sudo", "rm", self.output_image_file])

        # Create a new image file with the header
        with open(self.output_image_file, 'wb') as f:
            f.write(final_data)
        return self.output_image_file
    
    def image_header_split(self, input_file_path):
        # Read the header information
        with open(input_file_path, 'rb') as f:
            header_data = f.read(64)

        # Unpack the header data
        magic_number, self.image_type, image_size, self.auth_type, image_file_name = struct.unpack('IIII48s', header_data)

        # Check if the magic number is valid
        if magic_number != 0xAA55AA55:
            print(os.path.basename(input_file_path))
            return os.path.basename(input_file_path)

        # Extract and decode the image file name
        image_file_name = image_file_name.rstrip(b'\x00').decode('utf-8')

        # Read the image data
        image_data = open(input_file_path, 'rb').read()[64:]

        # Get the directory path of the input file
        output_directory = os.path.dirname(input_file_path)

        # Save the image to a new file using the extracted file name from the header
        output_image_path = os.path.join(output_directory, image_file_name)
        if os.path.isfile(output_image_path):
            subprocess.call(["sudo", "rm", output_image_path])
        
        with open(output_image_path, 'wb') as f:
            f.write(image_data)

        print(image_file_name)
        return image_file_name
              
"""
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
                                         MAIN FUNCTIONS STARTS BELOW
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
"""
if __name__ == "__main__":
    # print("Start to add/split the header to/from an image!!")
	
    parser = argparse.ArgumentParser(description='''Add/Split header!''')
    parser.add_argument('--operation', type=str, default="", action="store", dest='operation', help='Enter the operator {add_header | split_header}')
    parser.add_argument('--input_image_file', type=str, default="", action="store", dest='input_image_file', help='Enter the input image file path/name')
    parser.add_argument('--output_image_file', type=str, default="contents.xml", action="store", dest='output_image_file', help='Enter the output image file path/name')
    parser.add_argument('--image_type', type=str, default="0", action="store", dest='image_type', help='Enter the image type, 0: normal, 1:encrypted')
    parser.add_argument('--auth_type', type=str, default="1", action="store", dest='auth_type', help='Enter authentication type, 1:auth, 0:no_auth')
    parser.add_argument('--image_name', type=str, default="", action="store", dest='image_name', help='Enter image name')

    args=parser.parse_args()
    # print("The current arguments:"+args.manifest_xml+","+args.source_path+","+args.new_partition+','+args.chip_type)
    image_header_proc = image_header(args.input_image_file, args.output_image_file, args.image_type, args.auth_type, args.image_name)
    if args.operation == "add_header":
        new_image_name=image_header_proc.image_header_add()
    elif args.operation == "split_header":
        original_image_name=image_header_proc.image_header_split(args.input_image_file)
        sys.exit(original_image_name)
    else:
        print("Wrong operator, please enter { add_header | split_header}")
        sys.exit(631)
    sys.exit(0)
