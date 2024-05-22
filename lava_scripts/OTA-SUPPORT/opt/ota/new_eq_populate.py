# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 17:28:35 2022

@author: onkar.kadam@edgeq.io
"""

'''
Packages Used in the script
'''
import xml.etree.ElementTree as ET
import subprocess
import sys
import argparse
import os


''' Below class parses contents.xml file and writes script accordingly '''
class parsing:
    def __init__(self, contents_xml, new_located, new_folder, new_file_name, emmc_size):
        self.contents_xml = contents_xml
        self.new_located = new_located
        self.new_folder = new_folder
        self.new_file_name = new_file_name
        self.emmc_size = int(emmc_size)

    def dd_copy(self, device, sparse_file_name):
        subprocess.run(['sudo', 'dd', 'if=/mnt/dist/{0}'.format(sparse_file_name), 'of={0}'.format(device), 'bs=4M', 'status=progress'])

    def parser(self):
        try:
            # print("Parsing the Contents file.!")
            tree = ET.parse(self.contents_xml)
        except:
            print("Problems while loading the contents XML.!")
            sys.exit(1)
            
        root = tree.getroot()
        
        '''
        We are copying the tftp data on /tmp.
        This is a design decision and needs script changes in order to deployment
        '''
        if not os.path.exists("/tmp/mnt"):
            # print(f"Creating /tmp/mnt")
            os.makedirs("/tmp/mnt")
        rootfs_dev1="/dev/mmcblk0p13"
        rootfs_dev2="/dev/mmcblk0p14"
        for module in root.iter('module'):
            if self.new_located == "a_partition":
                # print("Mounting the partition A GUID {}".format(module.attrib.get("uuid_main")))
                device = subprocess.run("sudo sh ./mapping.sh -p {}".format(module.attrib.get("uuid_main")), shell=True, capture_output=True, text=True)
            elif self.new_located == "b_partition":
                # print("Mounting the partition B GUID {}".format(module.attrib.get("uuid_backup")))
                device = subprocess.run("sudo sh ./mapping.sh -p {}".format(module.attrib.get("uuid_backup")), shell=True, capture_output=True, text=True)
            else:
                print("Cannot support the location input"+self.new_located+" Please select {main or backup}")
            #device.wait()
            device = device.stdout
            device = device.strip('\n')
            # print("Current device: "+device)
            if (device is not None and self.emmc_size > 8):
                sparse_file_name = module.attrib['name']+'.sparse'
                print("Start to copy the sparse file: "+sparse_file_name+" to "+device)
                # print("Mounting {} on /tmp/mnt".format(device))
                # subprocess.run("sudo mount {} /tmp/mnt >/dev/null 2>&1 ".format(device), shell=True)
                # subprocess.run("sudo rm -rf /tmp/mnt/*", shell=True)
                # print("Start to copy to current partition: "+device+" ....")
                # for binary in module.iter("binary"):
                #   subprocess.run("mkdir -p $(dirname /tmp/mnt/{2}) && cp /tmp/{0}/{1} /tmp/mnt/{2}".format(module.attrib.get("source"), binary.attrib.get("file"), binary.attrib.get("destination")), shell=True)
                # subprocess.run("sync && sudo umount /tmp/mnt >/dev/null 2>&1", shell=True)
                self.dd_copy(device, sparse_file_name)
            else:            
                if (rootfs_dev1 not in device and  rootfs_dev2 not in device):
                    # print("Mounting {} on /tmp/mnt".format(device))
                    subprocess.run("sudo mount {} /tmp/mnt >/dev/null 2>&1 ".format(device), shell=True)
                    subprocess.run("sudo rm -rf /tmp/mnt/*", shell=True)
                    print("Start to copy to current partition: "+device+" ....")
                    for binary in module.iter("binary"):
                        subprocess.run("mkdir -p $(dirname /tmp/mnt/{2}) && cp /tmp/{0}/{1} /tmp/mnt/{2}".format(module.attrib.get("source"), binary.attrib.get("file"), binary.attrib.get("destination")), shell=True)
                    subprocess.run("sync && sudo umount /tmp/mnt >/dev/null 2>&1", shell=True)
                else:
                    # print("A0 will not support A/B partition for rootfs.tar yet")
                    None
            


                
"""
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
                                         MAIN FUNCTIONS STARTS BELOW
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
"""          
if __name__ == "__main__":
    # print("Creating factory flashing environment..!!")
	
    parser = argparse.ArgumentParser(description='''Factory Flasher.!''')
    parser.add_argument('--contents_xml', type=str, default="contents.xml", action="store", dest='contents_xml', help='Enter the location of the contents File')
    parser.add_argument('--new_located', type=str, default="a_partition", action="store", dest='new_located', help='Enter the location to emmc {a_partition|b_partition}')
    parser.add_argument('--new_folder', type=str, default="", action="store", dest='new_folder', help='Enter the location of new donwload folder')
    parser.add_argument('--new_file_name', type=str, default="", action="store", dest='new_file_name', help='Enter the filename in new donwload folder')
    parser.add_argument('--emmc_size', type=str, default="", action="store", dest='emmc_size', help='Enter the emmc size')
    args=parser.parse_args()
    # print("The current arguments:"+args.contents_xml+","+args.new_located)
    parse = parsing(args.contents_xml, args.new_located, args.new_folder, args.new_file_name, args.emmc_size)
    parse.parser()