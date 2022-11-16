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
pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_UL_c = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_UL_c, 0, 0, 900, 500, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)

pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)

handle_cmd_UL_c1 = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_UL_c1, 0, 500, 900, 500, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)

pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)

handle_cmd_UL_c2 = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_UL_c2, 1050, 0, 900, 500, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)

pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)

handle_cmd_UL_c3 = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_UL_c3, 1000, 500, 900, 500, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)
time.sleep(300)
# win32gui.CloseWindow(handle_cmd_UL_c)
# win32gui.CloseWindow(handle_cmd_UL_c1)

subprocess.call("taskkill /f /im powershell.exe", shell=True)

