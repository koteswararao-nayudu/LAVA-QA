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

time.sleep(2)

for x in range(100) :
    if str(x) == str(8) :
        print("equal")
    else :
        print("not equal")

