import pyautogui as pag
import time
import win32gui,win32con
import paramiko
from subprocess  import STDOUT
import os
import glob

time.sleep(2)

pag.FAILSAFE = False

def cleanup():
    x, y = pag.locateCenterOnScreen("command_bar.png", confidence=0.4)
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
    
    
    
    while True:
        try:
            conn = pag.getWindowsWithTitle("QXDM")[0].close()
            print(conn)
            if ( conn == None ) :
                break
            time.sleep(0.10)
        except IndexError:
            break



host = "192.168.3.106"
username = "equser"
password = "Password$2021"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
#_stdin, _stdout, _stderr = client.exec_command("lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board25/edgeq-raptor2_e2e_gnb_cellup_board41.yaml")
#_stdin, _stdout, _stderr = client.exec_command("lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board41/cell_attach_test/edgeq-raptor2_e2e_gnb_cellup_board41-generic.yaml")
#_stdin, _stdout, _stderr = client.exec_command("/usr/bin/python /lab-nfs/koti/cronjobs/GP_Build_trigger_cronjob.py & ")
#_stdin, _stdout,_stderr = client.exec_command(command)
#print("python script running in background")
#lava_job_id = _stdout.read().decode()
#print(lava_job_id)
#client.close()
#time.sleep(3)

#client = paramiko.SSHClient()
#client.connect(ip_address, username='root', pkey=paramiko_key, timeout=5)
transport = client.get_transport()
channel = transport.open_session()
channel.exec_command('/usr/bin/python3 /lab-nfs/koti/cronjobs/GP_Build_trigger_cronjob.py &')
#_stdin, _stdout, _stderr = channel.exec_command('lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board41/tmp/edgeq-raptor2_e2e_gnb_cellup_board41-generic.yaml')
#lava_job_id = _stdout.read().decode()
#print(lava_job_id)

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



print("Waiting for CELL UP")
flag1 = "true"
flag2 = ""
while [ True ]:
    print("1")
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

#time.sleep(0.5)
time.sleep(2)
pag.hotkey('winleft', 'd')
time.sleep(0.5)

pag.press("winleft", _pause=True)
time.sleep(0.5)

while True:
    try:
        conn = pag.getWindowsWithTitle("QXDM")[0].close()
        print(conn)
        if ( conn == None ) :
            break
        time.sleep(0.10)
        print("GetWindowswithtile for QXDM")
    except IndexError:
        break    

time.sleep(0.5)
pag.typewrite("QXDM",interval=0.2)
time.sleep(0.5)

pag.press("enter")
time.sleep(8)

handle = win32gui.GetForegroundWindow()
win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)
time.sleep(2)

pag.hotkey('ctrl', 'shift', 'w')
time.sleep(2)
pag.hotkey('ctrl', 'o')
time.sleep(0.5)
pag.typewrite("default.dmc",interval=0.2)
time.sleep(0.5)
pag.press("enter")
time.sleep(2)

file_path = "//192.168.3.230/public/lava-qa/results/windows-results/cell_attach.txt"


command_bar_flightmode_on = pag.locateCenterOnScreen("command_bar.png", confidence=0.4)
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


command_bar_flightmode_off = pag.locateCenterOnScreen("command_bar.png", confidence=0.4)
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

UE_registratioin = pag.locateCenterOnScreen("Registration_complete_RDP.png", confidence=0.5)
if UE_registratioin is None:
    print("Could not locate the UE_registratioin string")
else:
    x, y = UE_registratioin
    time.sleep(0.5)

pdu_session_establishment = pag.locateCenterOnScreen("pdu_session_establishment_RDP.png", confidence=0.5)
if pdu_session_establishment is None:
    print("Could not locate the PDU establishsment string")
    attach_file = open(file_path,'w')
    attach_file.write("fail")
    attach_file.close()
    cleanup()
    exit
else:
    x, y = pdu_session_establishment
    time.sleep(0.5)
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
    
    cmd_ipconfig_success = pag.locateCenterOnScreen("cmd_ipconfig_RDP.png", confidence=0.9)
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