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

targetipaddress="10.2.1.107"
appserveripaddress="192.168.2.84"

#Create DL and UL files
pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_DL_s = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_DL_s, 1050, 0, 900, 900, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)
    
pag.typewrite("Remove-Item C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt",interval=0.2)
pag.press("enter")
time.sleep(3)

pag.typewrite("Copy-Item -Path C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL-generic.txt -Destination C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt",interval=0.2)
pag.press("enter")
time.sleep(3)


# Read in the file
with open('C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('Target-IP', targetipaddress )

# Write the file out again
with open('file.txt', 'w') as file:
  file.write(filedata)




# pag.typewrite("\$koti=" + targetipaddress + ")
# pag.press("enter")
# time.sleep(3)

# pag.typewrite("(Get-Content C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt).Replace(\"TARGET-IP\", " +  str(targetipaddress) + " ) | Set-Content C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt",interval=0.2)
# pag.press("enter")
# time.sleep(3)