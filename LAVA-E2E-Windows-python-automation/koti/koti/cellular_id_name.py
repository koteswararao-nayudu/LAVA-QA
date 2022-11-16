import pyautogui as pag
import pyautogui
import time
import win32gui,win32con
import paramiko
from subprocess  import STDOUT
import os
import glob
from pathlib import Path
import subprocess
from paramiko import SSHClient, AutoAddPolicy
import serial


cellular_id_name = subprocess.Popen("grep \"Cellular\"  C:/Users/DELL/1.txt  | awk \"{$1=$2=$3=\\\"\\\"; print $0}\" | awk \"{$1=\\\"\\\";print $0}\" ", stdout=subprocess.PIPE, shell=True)
cellular_id_name_status = cellular_id_name.wait()
output_cellular_id_name, errors =  cellular_id_name.communicate()
print(output_cellular_id_name)
output_cellular_id_name_strip = output_cellular_id_name.strip().decode( "utf-8" )
print(output_cellular_id_name_strip)
print("Command exit status/return code : ", cellular_id_name_status)
