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
#floatip=float(targetipaddress)
appserveripaddress="192.168.2.84"

# # Read in the file
# with open('C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt', 'r') as file :
  # filedata = file.read()

# # Replace the target string
# filedata = filedata.replace("Target-IP", "targetipaddress" )

# # Write the file out again
# with open('file.txt', 'w') as file:
  # file.write(filedata)
  
f = open("C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt",'r')
filedata = f.read()
f.close()

newdata = filedata.replace("TARGET-IP", targetipaddress )

print(newdata)

f = open("C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt",'w')
f.write(newdata)
f.close()