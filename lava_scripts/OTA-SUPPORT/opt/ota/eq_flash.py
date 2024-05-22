# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 14:54:39 2022

@author: onkar.kadam@edgeq.io
"""

'''
Packages Used in the script
XML for parsing the partition.xml
sys for exiting for errors
argparse for providing paths of input and output
os for checking files and removing if needed
'''
import xml.etree.ElementTree as ET
import sys
import argparse
from os.path import exists
import os

''' Below class parses partition.xml file and writes partition table accordingly '''
class parsing:
    def __init__(self, partition_xml, partition_disk):
        self.partition_xml = partition_xml
        self.partition_disk = partition_disk
    
    '''
        The function parses elements of partition.xml and created a structure.
        From the xml element, we are creating a partition table script which will be used for partitioning.
        usage of output(considering default partition.disk):
            sfdik /dev/mmcblk0 < partition.disk
        Limitation: The script is designed around emmc and may need some upgrades for other devices
    '''
    def parser(self):
        try:
            print("Parsing the Partition XML file.!")
            tree = ET.parse(self.partition_xml)
        except:
            print("Problems while loading the Partition XML.!")
            sys.exit(1)
        
        ''' Accessing the cml elements '''
        root = tree.getroot()
        
        ''' Delete the older generated partition file if present '''
        if exists(self.partition_disk):
            print("Removing older Partition Script File..!!")
            os.remove(self.partition_disk)
         
        
        with open(self.partition_disk, "w+") as script:
            ''' Add partition method info '''
            for partition_table in root.iter('partition_table'):
                for element in ["label", "label-id", "device", "unit", "first-lba", "last-lba", "sector-size"]:
                    script.write("{0}: {1}\n".format(element, partition_table.attrib.get(element)))
            
            script.write("\n\n")
            
            part_num = 1
            ''' Add partitions to emmc as per partition.xml. Starting from mmcblk0. '''
            for element in root.iter('partition'):
                script.write("/dev/mmcblk0p{0} : start=        {1}, size=      {2}, type={3}, uuid={4}, name=\"{5}\"\n".format(part_num, 
                            element.attrib.get("start"), element.attrib.get("sector"), element.attrib.get("type"), element.attrib.get("guid"), 
                                element.attrib.get("label")))
                part_num +=1
                
"""
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
                                         MAIN FUNCTIONS STARTS BELOW
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
"""          
if __name__ == "__main__":
    print("Creating factory flashing environment..!!")
	
    ''' Parsing the arguments for Partition Table Script Generation '''
    parser = argparse.ArgumentParser(description='''Factory Flasher.!''')
    parser.add_argument('--partition_xml', type=str, default="partition.xml", action="store", dest='partition_xml', help='Enter the location of the partition File')
    parser.add_argument('--partition_disk', type=str, default="partition.disk", action="store", dest='partition_disk', help='Enter the location of the partition script File')
    args=parser.parse_args()
    
    ''' Accessing the parse function '''
    parse = parsing(args.partition_xml, args.partition_disk)
    parse.parser()