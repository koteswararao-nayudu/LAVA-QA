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


#Create DL and UL files
pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_DL_UL_files = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_DL_UL_files, 1050, 0, 900, 900, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)
    
pag.typewrite("cd Desktop/koti/koti/tmp/telit",interval=0.2)
pag.press("enter")
time.sleep(3)
    
pag.typewrite("./processkill.ps1 45679",interval=0.2)
pag.press("enter")
time.sleep(3)

