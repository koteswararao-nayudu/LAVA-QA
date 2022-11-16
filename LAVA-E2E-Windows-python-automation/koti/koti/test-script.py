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
    x, y = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar123.PNG', confidence=0.8)
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


timeout = 1800   # [seconds]
timeout_start1 = time.time()
print("#################")
print("timeout start1")
print(timeout_start1)
print("#################")

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(host, username=username, password=password)
sleeptime = 0.001
outdata, errdata = '', ''
ssh_transp = ssh.get_transport()
chan = ssh_transp.open_session()
# chan.settimeout(3 * 60 * 60)
chan.setblocking(0)
chan.exec_command(' /usr/bin/python3 /home/equser/koti/lava-testcases/cronjobs/GP_Build_trigger_cronjob.py >> /home/equser/koti/lava-testcases/cronjobs/GP_logs.txt' )
#chan.exec_command('ls -la')
print("Waiting for Jenkins Download complete")
while True:
    #while chan.recv_ready():
    #    outdata += chan.recv(1000)
    #while chan.recv_stderr_ready():
    #    errdata += chan.recv_stderr(1000)
    status=chan.exit_status_ready()
    #print(status)
    #print("Waiting for Jenkins Download complete")
    if chan.exit_status_ready(): # If completed
        if chan.recv_exit_status():
            print("we have not received any GP Build email and going to exit")
            exit()
        break

    if time.time() > timeout_start1 + timeout:
        print("Wget timeout after 30 min and going to exit")
        print(time.time())
        time.sleep(0.5)
        exit()


time.sleep(sleeptime)
retcode = chan.recv_exit_status()
print(retcode)
ssh_transp.close()



#print(outdata)
#print(errdata)

print("1st ssh complete")
#time.sleep(300)

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
#client.setblocking(0)
#_stdin, _stdout, _stderr = client.exec_command("lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.198/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board25/edgeq-raptor2_e2e_gnb_cellup_board41.yaml")
#_stdin, _stdout, _stderr = client.exec_command("lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.198/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board41/tmp/edgeq-raptor2_e2e_gnb_cellup_board41-generic1.yaml")
#_stdin, _stdout, _stderr = client.exec_command(" /usr/bin/python3 /home/equser/koti/lava-testcases/cronjobs/GP_Build_trigger_cronjob.py")

#exit_status = stdout.channel.recv_exit_status() 
#client.setblocking(1)
_stdin, _stdout1, _stderr = client.exec_command("lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.198/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board41/tmp/edgeq-raptor2_e2e_gnb_cellup_board41-generic1_RC2.yaml")
#_stdin, _stdout,_stderr = client.exec_command(command)
lava_job_id = _stdout1.read().decode()
print(lava_job_id)
client.close()


screenshot_path="\\\\192.168.3.230\\public\\lava-qa\\results\\screenshots"
print(os.listdir(screenshot_path))
os.chdir(screenshot_path)
cwd = os.getcwd() 
print("Current working directory is:", cwd)

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


timeout = 2400   # [seconds]
timeout_start = time.time()
print("#################")
print("timeout start")
print(timeout_start)
print("#################")

print("Waiting for CELL UP")
flag1 = "true"
flag2 = ""
while [ True ]:
    #print("1")
    #print("1-1")
    if os.path.exists(linux_results_file_path):
        print("2")
        f = open(linux_results_file_path, "r")
        string = "done"
        time.sleep(3)
        print("3")
        if string in f.read():
            flag2 = "true"
            print("CELL UP Done")
            break;
    
    if  flag1 == flag2:
        break
       
    if time.time() > timeout_start + timeout:
        print("timeouot before exit CELL_UP")
        print(time.time())
        time.sleep(0.5)
        exit()

time.sleep(2)
#time.sleep(2000)
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

myScreenshot = pyautogui.screenshot()
myScreenshot.save(os.path.join(cwd1,strip_str_lava_job_id + "_QXDM_application_open_status.jpg"))

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

file_path = "//192.168.3.230/public/lava-qa/results/windows-results/cell_attach.txt"


command_bar_flightmode_on = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar1.PNG', confidence=0.9)
if command_bar_flightmode_on is None:
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,strip_str_lava_job_id + "_QXDM_flight_mode_ON_bar_detection_FAIL.jpg"))
    time.sleep(2)
    print("Could not locate the flight mode on button")
    attach_file = open(file_path,'w')
    attach_file.write("fail")
    attach_file.close()
    cleanup()
    exit
else:
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,strip_str_lava_job_id + "_QXDM_flight_mode_ON_bar_detection_PASS.jpg"))
    time.sleep(2)
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
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,strip_str_lava_job_id + "_QXDM_flight_mode_OFF_bar_detection_FAIL.jpg"))
    time.sleep(2)
    print("Could not locate the flight mode off button")
    attach_file = open(file_path,'w')
    attach_file.write("fail")
    attach_file.close()
    cleanup()
    exit
else:
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,strip_str_lava_job_id + "_QXDM_flight_mode_OFF_bar_detection_PASS.jpg"))
    time.sleep(2)
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

UE_registratioin = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/Registration_complete_RDP1.PNG', confidence=0.5)
if UE_registratioin is None:
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,strip_str_lava_job_id + "_QXDM_UE_Registration_FAIL.jpg"))
    time.sleep(2)
    print("Could not locate the UE_registratioin string")
else:
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,strip_str_lava_job_id + "_QXDM_UE_Registration_PASS.jpg"))
    time.sleep(2)
    x, y = UE_registratioin
    time.sleep(0.5)

pdu_session_establishment = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/pdu_session_establishment_RDP1.PNG', confidence=0.5)
if pdu_session_establishment is None:
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,strip_str_lava_job_id + "_QXDM_session_establish_FAIL.jpg"))
    time.sleep(2)
    print("Could not locate the PDU establishsment string")
    attach_file = open(file_path,'w')
    attach_file.write("fail")
    attach_file.close()
    cleanup()
    exit
else:
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,strip_str_lava_job_id + "_QXDM_session_establish_PASS.jpg"))
    time.sleep(2)
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
    
    cmd_ipconfig_success = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/cmd_ipconfig_RDP12.PNG', confidence=0.9)
    if cmd_ipconfig_success is None:
        print("could not find the IP in cmd console")
        attach_file = open(file_path,'w')
        attach_file.write("fail")
        attach_file.close()
        cleanup()
        exit
    else:
        time.sleep(2)
        pag.click()
        time.sleep(2)
        pag.hotkey('alt', 'f4')
        time.sleep(3)
        attach_file = open(file_path,'w')
        attach_file.write("done")
        attach_file.close()
        cleanup()