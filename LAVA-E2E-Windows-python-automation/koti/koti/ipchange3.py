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

targetipaddress="10.2.1.153"
appserveripaddress="192.168.2.84"

pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("command Prompt",interval=0.1)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_UL_s1 = win32gui.GetForegroundWindow()
win32gui.ShowWindow(handle_cmd_UL_s1, win32con.SW_MAXIMIZE)
time.sleep(3)
    
#pag.typewrite("./Desktop/putty.exe -ssh equser@192.168.2.84 -pw Password$2021 -m C:\Users\DELL\Desktop\koti\koti\tmp\telit\DL.txt -t",interval=0.1)
pag.typewrite("cd Desktop/koti/koti/tmp/telit/",interval=0.3)
pag.press("enter")
time.sleep(3)

pag.typewrite("processkill.bat",interval=0.3)
pag.press("enter")
time.sleep(3)

win32gui.DestroyWindow(handle_cmd_UL_s1)

