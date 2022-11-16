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

file_path = "//192.168.3.230/public/lava-qa/results/windows-results/cell_attach.txt"
file_path_attach_detach_stress = "//192.168.3.230/public/lava-qa/results/windows-results/cell_attach_detach_stress.txt"

output_telit_ipaddress_strip=""
#targetipaddress = output_telit_ipaddress.strip().decode( "utf-8" )
appserveripaddress="192.168.2.84"
nullstring=""

if output_telit_ipaddress_strip == nullstring :
    while True :
        print("test fail")
        print("Could not locate the IP Address")
        attach_file = open(file_path_attach_detach_stress,'w')
        attach_file.write("pass")
        attach_file.close()
        time.sleep(10)