import pyautogui as pag
import pyautogui
import time
import win32gui,win32con
import paramiko
from subprocess  import STDOUT
import os
import glob
from pathlib import Path

time.sleep(2)


import subprocess
subprocess.call("taskkill /f /im qxdm.exe", shell=True)
#count=pag.getWindowsWithTitle("QXDM")[0]
#print(count)

#while True:
#    try:
        #conn = pag.getWindowsWithTitle("QXDM")[0].close()
        #print(conn)
#        if ( conn == None ) :
#            break
#        time.sleep(0.10)
#    except IndexError:
#        break

#time.sleep(0.5)
time.sleep(2)
pag.hotkey('winleft', 'd')
time.sleep(0.5)

pag.press("winleft", _pause=True)
time.sleep(0.5)

# while True:
    # try:
        # conn = pag.getWindowsWithTitle("QXDM")[0].close()
        # print(conn)
        # if ( conn == None ) :
            # break
        # time.sleep(0.10)
        # print("GetWindowswithtile for QXDM")
    # except IndexError:
        # break    

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
pag.typewrite("C:\\Users\\equser\\Desktop\\koti\\default.dmc",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(2)

file_path = "//192.168.3.230/public/lava-qa/results/windows-results/cell_attach.txt"


command_bar_flightmode_on = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar.png', confidence=0.4)
if command_bar_flightmode_on is None:
    print("Could not locate the flight mode on button")
    attach_file = open(file_path,'w')
    attach_file.write("fail")
    attach_file.close()
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


command_bar_flightmode_off = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar.png', confidence=0.4)
if command_bar_flightmode_off is None:
    print("Could not locate the flight mode off button")
    attach_file = open(file_path,'w')
    attach_file.write("fail")
    attach_file.close()
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



subprocess.call("taskkill /f /im qxdm.exe", shell=True)