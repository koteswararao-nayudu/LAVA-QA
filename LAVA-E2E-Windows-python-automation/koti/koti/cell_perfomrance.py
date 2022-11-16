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

targetipaddress="10.2.1.169"
appserveripaddress="192.168.2.84"


cwd1 = os.getcwd() 
# print the current directory
print("Current working directory is:", cwd1)

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
    
pag.typewrite("Remove-Item C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt",interval=0.2)
pag.press("enter")
time.sleep(3)

pag.typewrite("Copy-Item -Path C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL-generic.txt -Destination C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt",interval=0.2)
pag.press("enter")
time.sleep(3)


f = open("C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt",'r')
filedata = f.read()
f.close()

newdata = filedata.replace("TARGET-IP", targetipaddress )

print(newdata)

f = open("C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt",'w')
f.write(newdata)
f.close()


pag.typewrite("Remove-Item C:/Users/DELL/Desktop/koti/koti/tmp/telit/UL.txt",interval=0.2)
pag.press("enter")
time.sleep(3)

pag.typewrite("Copy-Item -Path C:/Users/DELL/Desktop/koti/koti/tmp/telit/UL-generic.txt -Destination C:/Users/DELL/Desktop/koti/koti/tmp/telit/UL.txt",interval=0.2)
pag.press("enter")
time.sleep(3)


f = open("C:/Users/DELL/Desktop/koti/koti/tmp/telit/UL.txt",'r')
filedata = f.read()
f.close()

newdata = filedata.replace("TARGET-IP", targetipaddress )

print(newdata)

f = open("C:/Users/DELL/Desktop/koti/koti/tmp/telit/UL.txt",'w')
f.write(newdata)
f.close()

time.sleep(5)
win32gui.CloseWindow(handle_cmd_DL_UL_files)

#DL:
############################

#print("test pass")
pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("command Prompt",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_DL_c = win32gui.GetForegroundWindow()
win32gui.ShowWindow(handle_cmd_DL_c, win32con.SW_MAXIMIZE)
time.sleep(3)
    
#pag.typewrite("./Desktop/putty.exe -ssh equser@192.168.2.84 -pw Password$2021 -m C:\Users\DELL\Desktop\koti\koti\tmp\telit\DL.txt -t",interval=0.2)
pag.typewrite("putty.exe -ssh equser@" + appserveripaddress + " -pw Password$2021 -m C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt -t",interval=0.2)
pag.press("enter")
time.sleep(5)

handle_cmd_DL_c_putty = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_DL_c_putty, 0, 0, 850, 450, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)

pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_DL_s = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_DL_s, 1050, 0, 850, 450, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)
    
pag.typewrite("./Desktop/iperf-2.1.5-win.exe -s -u -i 1 -t 300 -p 45679 -l 1400",interval=0.2)
pag.press("enter")
time.sleep(3)

time.sleep(30)
print("Taking screenshot")
myScreenshot = pyautogui.screenshot()
time.sleep(2)
myScreenshot.save(os.path.join(cwd1,"DL_Performance.jpg"))

time.sleep(60)

win32gui.CloseWindow(handle_cmd_DL_c)
win32gui.CloseWindow(handle_cmd_DL_s)

subprocess.call("taskkill /f /im putty.exe", shell=True)
subprocess.call("taskkill /f /im powershell.exe", shell=True)

#UL
#######################
pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("command Prompt",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_UL_s = win32gui.GetForegroundWindow()
win32gui.ShowWindow(handle_cmd_UL_s, win32con.SW_MAXIMIZE)
time.sleep(3)
    
#pag.typewrite("./Desktop/putty.exe -ssh equser@192.168.2.84 -pw Password$2021 -m C:\Users\DELL\Desktop\koti\koti\tmp\telit\DL.txt -t",interval=0.2)
pag.typewrite("putty.exe -ssh equser@" + appserveripaddress + " -pw Password$2021 -m C:/Users/DELL/Desktop/koti/koti/tmp/telit/UL.txt -t",interval=0.2)
pag.press("enter")
time.sleep(3)

handle_cmd_UL_s_putty = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_UL_s_putty, 0, 480, 850, 450, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)

pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_UL_c = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_UL_c, 1000, 480, 850, 450, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)
    
pag.typewrite("./Desktop/iperf-2.1.5-win.exe -c 192.168.2.84 -u -i 1 -p 45679 -t 300 -l 1400 -B " + targetipaddress + " -b 50m",interval=0.2)
pag.press("enter")
time.sleep(3)

time.sleep(30)
print("Taking screenshot")
myScreenshot = pyautogui.screenshot()
time.sleep(2)
myScreenshot.save(os.path.join(cwd1,"UL_Performance.jpg"))
time.sleep(2)
time.sleep(60)

win32gui.CloseWindow(handle_cmd_UL_c)
win32gui.CloseWindow(handle_cmd_UL_s)

subprocess.call("taskkill /f /im putty.exe", shell=True)
subprocess.call("taskkill /f /im powershell.exe", shell=True)

#Bi-Direcional
############################

#print("test pass")
pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("command Prompt",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_DL_c_bidi = win32gui.GetForegroundWindow()
win32gui.ShowWindow(handle_cmd_DL_c_bidi, win32con.SW_MAXIMIZE)
time.sleep(3)
    
#pag.typewrite("./Desktop/putty.exe -ssh equser@192.168.2.84 -pw Password$2021 -m C:\Users\DELL\Desktop\koti\koti\tmp\telit\DL.txt -t",interval=0.2)
pag.typewrite("putty.exe -ssh equser@" + appserveripaddress + " -pw Password$2021 -m C:/Users/DELL/Desktop/koti/koti/tmp/telit/DL.txt -t",interval=0.2)
pag.press("enter")
time.sleep(5)

handle_cmd_DL_c_putty_bidi = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_DL_c_putty_bidi, 0, 0, 850, 450, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)

pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_DL_s_bidi = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_DL_s_bidi, 1050, 0, 850, 450, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)
    
pag.typewrite("./Desktop/iperf-2.1.5-win.exe -s -u -i 1 -t 300 -p 45679 -l 1400",interval=0.2)
pag.press("enter")
time.sleep(3)

#time.sleep(30)
#print("Taking screenshot")
#myScreenshot = pyautogui.screenshot()
#time.sleep(2)
#myScreenshot.save(os.path.join(cwd1,"DL_PASS.jpg"))

#time.sleep(60)

#win32gui.CloseWindow(handle_cmd_DL_c)
#win32gui.CloseWindow(handle_cmd_DL_s)

#subprocess.call("taskkill /f /im putty.exe", shell=True)
#subprocess.call("taskkill /f /im powershell.exe", shell=True)

#UL
#######################
pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("command Prompt",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_UL_s_bidi = win32gui.GetForegroundWindow()
win32gui.ShowWindow(handle_cmd_UL_s_bidi, win32con.SW_MAXIMIZE)
time.sleep(3)
    
#pag.typewrite("./Desktop/putty.exe -ssh equser@192.168.2.84 -pw Password$2021 -m C:\Users\DELL\Desktop\koti\koti\tmp\telit\DL.txt -t",interval=0.2)
pag.typewrite("putty.exe -ssh equser@" + appserveripaddress + " -pw Password$2021 -m C:/Users/DELL/Desktop/koti/koti/tmp/telit/UL.txt -t",interval=0.2)
pag.press("enter")
time.sleep(3)

handle_cmd_UL_s_putty_bidi = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_UL_s_putty_bidi, 0, 480, 850, 450, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)

pag.press("winleft", _pause=True)
time.sleep(1)
pag.typewrite("windows PowerShell",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(4)
    
handle_cmd_UL_c_bidi = win32gui.GetForegroundWindow()
win32gui.MoveWindow(handle_cmd_UL_c_bidi, 1000, 480, 850, 450, True)
#win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
time.sleep(3)
    
pag.typewrite("./Desktop/iperf-2.1.5-win.exe -c 192.168.2.84 -u -i 1 -p 45679 -t 300 -l 1400 -B " + targetipaddress + " -b 50m",interval=0.2)
pag.press("enter")
time.sleep(3)

time.sleep(30)
print("Taking screenshot")
myScreenshot = pyautogui.screenshot()
time.sleep(2)
myScreenshot.save(os.path.join(cwd1,"UL_PASS.jpg"))
time.sleep(2)
time.sleep(100)

print("Taking screenshot")
myScreenshot = pyautogui.screenshot()
time.sleep(2)
myScreenshot.save(os.path.join(cwd1,"Bidirectional_Performance.jpg"))
time.sleep(2)
time.sleep(60)

win32gui.CloseWindow(handle_cmd_UL_c_bidi)
win32gui.CloseWindow(handle_cmd_UL_s_bidi)


subprocess.call("taskkill /f /im putty.exe", shell=True)
subprocess.call("taskkill /f /im powershell.exe", shell=True)



# telit_ipaddress = subprocess.Popen("grep \"IP Address\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt | awk \"{ print $3 }\"", stdout=subprocess.PIPE, shell=True)
# telit_ipaddress_status = telit_ipaddress.wait()
# output_telit_ipaddress, errors =  telit_ipaddress.communicate()
# print(output_telit_ipaddress)
# output_telit_ipaddress_strip = output_telit_ipaddress.strip().decode( "utf-8" )
# print(output_telit_ipaddress_strip)
# print("Command exit status/return code : ", telit_ipaddress_status)

# host = "192.168.2.84"
# username = "equser"
# password = "Password$2021"

# timeout = 5400   # [seconds]
# timeout_start1 = time.time()
# print("#################")
# print("timeout start1")
# print(timeout_start1)
# print("#################")

# ssh = SSHClient()
# ssh.set_missing_host_key_policy(AutoAddPolicy())
# ssh.connect(host, username=username, password=password)
# sleeptime = 0.001
# outdata, errdata = '', ''
# ssh_transp = ssh.get_transport()
# chan = ssh_transp.open_session()
# # chan.settimeout(3 * 60 * 60)
# chan.setblocking(0)
# chan.exec_command('iperf -c 10.2.1.107 -u -i 1 -p 45679 -t 100 -l 1400 -B 192.168.2.84 -b 400m ' )
# #chan.exec_command('ls -la')
# print("Waiting for Jenkins Download complete")

# time.sleep(sleeptime)
# retcode = chan.recv_exit_status()
# print(retcode)
# ssh_transp.close()

# # client = paramiko.client.SSHClient()
# # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # client.connect(host, username=username, password=password)
# # #client.setblocking(0)
# # _stdin, _stdout1, _stderr = client.exec_command(")
# # #_stdin, _stdout,_stderr = client.exec_command(command)
# # lava_job_id = _stdout1.read().decode()
# # print(lava_job_id)
# # client.close()