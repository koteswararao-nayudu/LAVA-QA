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


telit_ipaddress = subprocess.Popen("grep \"IP Address\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt | awk \"{ print $3 }\"", stdout=subprocess.PIPE, shell=True)
telit_ipaddress_status = telit_ipaddress.wait()
output_telit_ipaddress, errors =  telit_ipaddress.communicate()
print(output_telit_ipaddress)
clean_line = output_telit_ipaddress.strip().decode( "utf-8" )
print(clean_line)
print("Command exit status/return code : ", telit_ipaddress_status)
print("Command exit status/return code : ", telit_ipaddress.returncode)
#print("output ", telit_ipaddress.check_output)

nullstring=""

if clean_line == nullstring :
    print("null")
else:
    print("string")


rc, out = subprocess.getstatusoutput("grep \"IP Address\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt | awk \"{ print $3 }\"")

print(rc)
print(out)

if True :
    print("pass")
else:
    print("fail")
    
    
if os.system("grep -w \"Telit Serial Auxiliary Interface\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt"):
    print("telit port is not available")
else:
    print("Telit port is available")
    
x = os.system("grep -w \"Telit Serial Auxiliary Interface\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt")
print(x)


com_string = subprocess.Popen("grep -w \"Telit Serial Auxiliary Interface\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt | awk \"{ print $1 }\" | awk -F \"=\" \"{ print $1 }\"", stdout=subprocess.PIPE, shell=True)
com_string_status = com_string.wait()
output_com_string, errors =  com_string.communicate()
print(output_com_string)
com_string_strip = output_com_string.strip().decode( "utf-8" )
print(com_string_strip)
print("Command exit status/return code : ", com_string_status)


