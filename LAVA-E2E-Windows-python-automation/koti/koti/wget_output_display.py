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

time.sleep(2)

pag.FAILSAFE = False

def cleanup():
    x, y = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar.png', confidence=0.4)
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
    # while True:
        # try:
            # conn = pag.getWindowsWithTitle("QXDM")[0].close()
            # print(conn)
            # if ( conn == None ) :
                # break
            # time.sleep(0.10)
        # except IndexError:
            # break



host = "192.168.3.198"
username = "equser"
password = "Password$2021"

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(host, username=username, password=password)
sleeptime = 0.001
outdata, errdata = '', ''
ssh_transp = ssh.get_transport()
chan = ssh_transp.open_session()
# chan.settimeout(3 * 60 * 60)
chan.setblocking(0)
#_stdin, _stdout1, _stderr = chan.exec_command(' /usr/bin/python3 /home/equser/koti/lava-testcases/cronjobs/GP_Build_trigger_cronjob.py' )
chan.exec_command(' /usr/bin/python3 /home/equser/koti/lava-testcases/cronjobs/GP_Build_trigger_cronjob.py' )
#lava_job_id = _stdout1.read().decode()
#chan.exec_command('ls -la')
while True:
    #while chan.recv_ready():
    #    outdata += chan.recv(1000)
    #while chan.recv_stderr_ready():
    #    errdata += chan.recv_stderr(1000)
    #print(chan.recv_stderr(100))
    status=chan.exit_status_ready()
    print(status)
    if chan.exit_status_ready(): # If completed
        #print(lava_job_id)
        break
time.sleep(sleeptime)
retcode = chan.recv_exit_status()
print(retcode)
ssh_transp.close()

