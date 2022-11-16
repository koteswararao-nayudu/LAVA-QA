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

sec = input('Let us wait for user input. Let me know how many seconds to sleep now.\n')
print('Going to sleep for', sec, 'seconds.')
time.sleep(int(sec))
print('Enough of sleeping, I Quit!')