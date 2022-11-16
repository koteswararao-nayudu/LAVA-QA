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


#check for Telit connection
if os.path.exists("C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt"):
    os.remove("C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt")


os.system("C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_port_names.bat >> C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt ")

p = subprocess.Popen("grep -w \"Telit Serial Auxiliary Interface\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt", stdout=subprocess.PIPE, shell=True)
p_status = p.wait()
(output, err) = p.communicate()
#print(output)
print("Command exit status/return code : ", p_status)



if os.system("grep -w \"Telit Serial Auxiliary Interface\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt"):
    print("telit port is not available")
else:
    print("Telit port is available")
    
com_string = subprocess.Popen("grep -w \"Telit Serial Auxiliary Interface\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt | awk \"{ print $1 }\" | awk -F \"=\" \"{ print $1 }\"", stdout=subprocess.PIPE, shell=True)
com_string_status = com_string.wait()
output_com_string, errors =  com_string.communicate()
print(output_com_string)
com_string_strip = output_com_string.strip().decode( "utf-8" )
print(com_string_strip)
print("Command exit status/return code : ", com_string_status)


port = serial.Serial(com_string_strip, baudrate=115200, timeout=3.0)

#while True:
port.write(b"at \r\n")
port.flush()
rcv1 = port.read(20)
rcv1_strip=rcv1.strip().decode( "utf-8" )
print(repr(rcv1_strip))
port.write(b"at+cfun=0 \r\n")
rcv2 = port.read(80)
rcv2_strip=rcv2.strip().decode( "utf-8" )
print(repr(rcv2_strip))

screenshot_path="\\\\192.168.3.230\\public\\lava-qa\\results\\screenshots"
print(os.listdir(screenshot_path))
os.chdir(screenshot_path)
cwd = os.getcwd() 
print("Current working directory is:", cwd)

lava_job_id=12345
str_lava_job_id=str(lava_job_id)
strip_str_lava_job_id = str_lava_job_id.strip('\n')
joinpath = os.path.join(cwd, strip_str_lava_job_id)
print(joinpath)
access_rights = 0o777
os.mkdir(joinpath, access_rights )
chdirvar=os.chdir(joinpath)
print(chdirvar)
cwd1 = os.getcwd() 
# print the current directory
print("Current working directory is:", cwd1)


linux_results_file_path = "//192.168.3.230/public/lava-qa/results/linux-results/cell_up_status.txt"
linux_results_file_path_job_id = "//192.168.3.230/public/lava-qa/results/linux-results/job_id.txt"
windows_results_file_path = "//192.168.3.230/public/lava-qa/results/windows-results/cell_attach.txt"

if os.path.exists(linux_results_file_path): 
    os.remove(linux_results_file_path)
else:
    print("Does not find the file")

if os.path.exists(linux_results_file_path_job_id): 
    os.remove(linux_results_file_path_job_id)
else:
    print("Does not find the file")


if os.path.exists(windows_results_file_path):
    os.remove(windows_results_file_path)
else:
    print("Does not find the file")


text_file = open(linux_results_file_path_job_id, "w")
n = text_file.write(strip_str_lava_job_id)
text_file.close()

time.sleep(10)
timeout = 2400   # [seconds]
timeout_start = time.time()
print("#################")
print("timeout start")
print(timeout_start)
print("#################")

print("Waiting for CELL UP")
flag1 = "true"
flag2 = ""


#time.sleep(300)

print("test pass")
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
pag.press("enter")
time.sleep(2)
print("Taking screenshot")
myScreenshot = pyautogui.screenshot()
time.sleep(2)
myScreenshot.save(os.path.join(cwd1,"1_" + strip_str_lava_job_id + "_ipconfig_PASS.jpg"))
time.sleep(2)



