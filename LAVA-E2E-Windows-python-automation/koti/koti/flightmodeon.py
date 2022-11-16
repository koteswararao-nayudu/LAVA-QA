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


time.sleep(2)

subprocess.call("taskkill /f /im qxdm.exe", shell=True)


def cleanup():
    x, y = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar1.PNG', confidence=0.9)
    print (x, y)
    time.sleep(0.5)
    pag.moveTo(x, y, 1)
    time.sleep(0.5)
    pag.click()
    time.sleep(2)

    pag.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pag.hotkey('del')
    time.sleep(0.5)
    pag.typewrite("mode lpm",interval=0.2)
    time.sleep(0.5)
    pag.press("enter")
    time.sleep(5)
    
    
    
    
    subprocess.call("taskkill /f /im qxdm.exe", shell=True)

time.sleep(2)
#time.sleep(2000)
pag.hotkey('winleft', 'd')
time.sleep(0.5)

pag.press("winleft", _pause=True)
time.sleep(0.5)

time.sleep(0.5)
pag.typewrite("QXDM",interval=0.2)
time.sleep(0.5)

pag.press("enter")
time.sleep(25)

handle = win32gui.GetForegroundWindow()
win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)
time.sleep(2)

pag.hotkey('ctrl', 'shift', 'w')
time.sleep(2)
pag.hotkey('ctrl', 'o')
time.sleep(0.5)
pag.typewrite("C:\\Users\\equser\\Desktop\\koti\\default1.dmc",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(2)


command_bar_flightmode_on = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar1.PNG', confidence=0.9)
if command_bar_flightmode_on is None:
    print("Could not locate the flight mode on button")
    cleanup()
    exit
else:
    x, y = command_bar_flightmode_on
    time.sleep(0.5)
    pag.moveTo(x, y, 1)
    time.sleep(0.5)
    pag.click()
    time.sleep(2)

    pag.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pag.hotkey('del')
    time.sleep(0.5)
    pag.typewrite("mode lpm",interval=0.2)
    time.sleep(0.5)
    pag.press("enter")
    time.sleep(5)


command_bar_flightmode_off = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar1.PNG', confidence=0.9)
if command_bar_flightmode_off is None:
    print("Could not locate the flight mode off button")
    cleanup()
    exit
else:
    x, y = command_bar_flightmode_off
    time.sleep(0.5)
    pag.moveTo(x, y, 1)
    time.sleep(0.5)
    pag.click()
    time.sleep(2)

    pag.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pag.hotkey('del')
    time.sleep(0.5)
    pag.typewrite("mode online",interval=0.2)
    time.sleep(0.5)
    pag.press("enter")
    time.sleep(10)

UE_registratioin = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/Registration_complete_RDP.png', confidence=0.5)
if UE_registratioin is None:
    print("Could not locate the UE_registratioin string")
else:
    x, y = UE_registratioin
    time.sleep(0.5)

pdu_session_establishment = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/pdu_session_establishment_RDP.png', confidence=0.5)
if pdu_session_establishment is None:
    print("Could not locate the PDU establishsment string")
    cleanup()
    exit
else:
    x, y = pdu_session_establishment
    time.sleep(2)
    pag.press("winleft", _pause=True)
    time.sleep(1)
    pag.typewrite("command Prompt",interval=0.2)
    time.sleep(0.5)
    
    pag.press("enter")
    time.sleep(3)
    
    handle_cmd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
    time.sleep(3)
    
    time.sleep(0.5)
    pag.typewrite("ipconfig",interval=0.2)
    time.sleep(0.5)
    
    pag.press("enter")
    time.sleep(3)
    
    cmd_ipconfig_success = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/cmd_ipconfig_RDP.png', confidence=0.9)
    if cmd_ipconfig_success is None:
        print("could not find the IP in cmd console")
        cleanup()
        exit
    else:
        time.sleep(2)
        pag.click()
        time.sleep(2)
        pag.hotkey('alt', 'f4')
        time.sleep(3)
        cleanup()