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

#subprocess.call("taskkill /f /im qxdm.exe", shell=True)

time.sleep(20)

# pag.press("winleft", _pause=True)
# time.sleep(0.5)

# time.sleep(0.5)
# pag.typewrite("QXDM",interval=0.2)
# time.sleep(0.5)

# pag.press("enter")
# time.sleep(25)

# bartmp = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar1.PNG', confidence=0.8)
# x, y = bartmp
# print (x, y)
# time.sleep(0.5)
# pag.moveTo(x, y, 1)
# time.sleep(0.5)
# pag.click()
# time.sleep(2)
# pag.hotkey('ctrl', 'a')
# time.sleep(0.5)
# pag.hotkey('del')
# time.sleep(0.5)
# pag.typewrite("mode lpm",interval=0.2)
# time.sleep(0.5)
# pag.press("enter")
# time.sleep(10)

# time.sleep(10)

# subprocess.call("taskkill /f /im qxdm.exe", shell=True)

# time.sleep(20)
# exit()

# pag.FAILSAFE = False

# def cleanup():
    # x, y = pag.locateCenterOnScreen('C:/Users/equser/Desktop/koti/koti/koti/command_bar123.PNG', confidence=0.8)
    # print (x, y)
    # time.sleep(0.5)
    # pag.moveTo(x, y, 1)
    # time.sleep(0.5)
    # pag.click()
    # time.sleep(2)

    # pag.hotkey('ctrl', 'a')
    # time.sleep(0.5)
    # pag.hotkey('del')
    # time.sleep(0.5)
    # pag.typewrite("mode lpm",interval=0.2)
    # time.sleep(0.5)
    # pag.press("enter")
    # time.sleep(5)
    
    
    
    
    # subprocess.call("taskkill /f /im qxdm.exe", shell=True)
    # # while True:
        # # try:
            # # conn = pag.getWindowsWithTitle("QXDM")[0].close()
            # # print(conn)
            # # if ( conn == None ) :
                # # break
            # # time.sleep(0.10)
        # # except IndexError:
            # # break

#check for Telit connection
nullstring=""

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
    exit
else:
    print("Telit port is available")
    
com_string = subprocess.Popen("grep -w \"Telit Serial Auxiliary Interface\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt | awk \"{ print $1 }\" | awk -F \"=\" \"{ print $1 }\"", stdout=subprocess.PIPE, shell=True)
com_string_status = com_string.wait()
output_com_string, errors =  com_string.communicate()
print(output_com_string)
com_string_strip = output_com_string.strip().decode( "utf-8" )
print(com_string_strip)
print("Command exit status/return code : ", com_string_status)

if com_string_strip == nullstring :
    print("failed to fetch COM Port number")
    exit
    

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
# pag.press("winleft", _pause=True)
# time.sleep(0.5)

# time.sleep(0.5)
# pag.typewrite("QXDM",interval=0.2)
# time.sleep(0.5)

# pag.press("enter")
# time.sleep(25)

# cleanup()
# exit()

host = "192.168.3.198"
username = "equser"
password = "Password$2021"


timeout = 5400   # [seconds]
timeout_start1 = time.time()
print("#################")
print("timeout start1")
print(timeout_start1)
print("#################")

# ssh = SSHClient()
# ssh.set_missing_host_key_policy(AutoAddPolicy())
# ssh.connect(host, username=username, password=password)
# sleeptime = 0.001
# outdata, errdata = '', ''
# ssh_transp = ssh.get_transport()
# chan = ssh_transp.open_session()
# # chan.settimeout(3 * 60 * 60)
# chan.setblocking(0)
# chan.exec_command(' /usr/bin/python3 /home/equser/koti/lava-testcases/cronjobs/GP_Build_trigger_cronjob.py >> /home/equser/koti/lava-testcases/cronjobs/GP_logs_RC6.txt' )
# #chan.exec_command('ls -la')
# print("Waiting for Jenkins Download complete")
# while True:
    # #while chan.recv_ready():
    # #    outdata += chan.recv(1000)
    # #while chan.recv_stderr_ready():
    # #    errdata += chan.recv_stderr(1000)
    # status=chan.exit_status_ready()
    # #print(status)
    # #print("Waiting for Jenkins Download complete")
    # if chan.exit_status_ready(): # If completed
        # if chan.recv_exit_status():
            # print("we have not received any GP Build email and going to exit")
            # exit()
        # break

    # if time.time() > timeout_start1 + timeout:
        # print("Wget timeout after 30 min and going to exit")
        # print(time.time())
        # time.sleep(0.5)
        # exit()


# time.sleep(sleeptime)
# retcode = chan.recv_exit_status()
# print(retcode)
# ssh_transp.close()



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
#_stdin, _stdout1, _stderr = client.exec_command("lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.198/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board41/tmp/edgeq-raptor2_e2e_gnb_cellup_board41-generic1_RC5.1.yaml")
_stdin, _stdout1, _stderr = client.exec_command("lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.198/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board46/tmp/edgeq-raptor2_e2e_gnb_cellup_board46-generic1_RC6.yaml")
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





port.write(b"at \r\n")
rcv3 = port.read(80)
rcv3_strip=rcv3.strip().decode( "utf-8" )
print(repr(rcv3_strip))
port.write(b"at+cfun=0 \r\n")
rcv4 = port.read(80)
rcv4_strip=rcv4.strip().decode( "utf-8" )
print(repr(rcv4_strip))
time.sleep(15)
port.write(b"at+cfun=1 \r\n")
time.sleep(1)
rcv5 = port.read(82)
rcv5_strip=rcv5.strip().decode( "utf-8" )
print(repr(rcv5_strip))

print("wait few minutes to assign IP for UE")
#time.sleep(240)
time.sleep(180)

if os.path.exists("C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt"):
    print("Removing ipaddress_file.txt")
    os.remove("C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt")


netshcmd = subprocess.Popen("netsh interface ipv4 show addresses \"Cellular\" >> C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt ", stdout=subprocess.PIPE, shell=True)
netshcmd_status = netshcmd.wait()
output_netshcmd, errors =  netshcmd.communicate()
print(output_netshcmd)
print("Command exit status/return code : ", netshcmd_status)
#ipp = subprocess.Popen(netsh show >> C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt )

#if os.path.exists("C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt"):
#    os.remove("C:/Users/DELL/Desktop/koti/koti/tmp/telit/serial_ports.txt")

telit_ipaddress = subprocess.Popen("grep \"IP Address\" C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt | awk \"{ print $3 }\"", stdout=subprocess.PIPE, shell=True)
telit_ipaddress_status = telit_ipaddress.wait()
output_telit_ipaddress, errors =  telit_ipaddress.communicate()
print(output_telit_ipaddress)
output_telit_ipaddress_strip = output_telit_ipaddress.strip().decode( "utf-8" )
print(output_telit_ipaddress_strip)
print("Command exit status/return code : ", telit_ipaddress_status)


file_path = "//192.168.3.230/public/lava-qa/results/windows-results/cell_attach.txt"

targetipaddress = output_telit_ipaddress.strip().decode( "utf-8" )
appserveripaddress="192.168.2.84"


if output_telit_ipaddress_strip == nullstring :
    print("test fail")
    print("Could not locate the IP Address")
    attach_file = open(file_path,'w')
    attach_file.write("fail")
    attach_file.close()
else:
    print("test pass")
    pag.press("winleft", _pause=True)
    time.sleep(1)
    pag.typewrite("command Prompt",interval=0.2)
    time.sleep(0.5)
    pag.press("enter")
    time.sleep(4)
    
    pag.typewrite("cd Desktop/koti/koti/tmp/telit/",interval=0.3)
    pag.press("enter")
    time.sleep(3)

    pag.typewrite("processkill.bat",interval=0.3)
    pag.press("enter")
    time.sleep(3)
    
    pag.typewrite("exit",interval=0.3)
    pag.press("enter")
    time.sleep(3)
    
    print("test pass")
    pag.press("winleft", _pause=True)
    time.sleep(1)
    pag.typewrite("command Prompt",interval=0.2)
    time.sleep(0.5)
    pag.press("enter")
    time.sleep(4)
    
    handle_cmd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(handle_cmd, win32con.SW_MAXIMIZE)
    time.sleep(3)
    
    pag.typewrite("ipconfig",interval=0.2)
    pag.press("enter")
    time.sleep(3)
    
    
    
    #time.sleep(0.5)
    
    #pag.press("enter")
    #time.sleep(2)
    print("Taking screenshot")
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,"1_" + strip_str_lava_job_id + "_ipconfig_PASS.jpg"))
    time.sleep(2)


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
        
    pag.typewrite("./Desktop/iperf-2.1.5-win.exe -s -u -i 1 -t 3000 -p 45679 -l 1400",interval=0.2)
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

    pag.press("winleft", _pause=True)
    time.sleep(1)
    pag.typewrite("command Prompt",interval=0.2)
    time.sleep(0.5)
    pag.press("enter")
    time.sleep(4)
    
    pag.typewrite("cd Desktop/koti/koti/tmp/telit/",interval=0.3)
    pag.press("enter")
    time.sleep(3)

    pag.typewrite("processkill.bat",interval=0.3)
    pag.press("enter")
    time.sleep(3)
    
    pag.typewrite("exit",interval=0.3)
    pag.press("enter")
    time.sleep(3)
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
        
    pag.typewrite("./Desktop/iperf-2.1.5-win.exe -c 192.168.2.84 -u -i 1 -p 45679 -t 3000 -l 1400 -B " + targetipaddress + " -b 50m",interval=0.2)
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

    pag.press("winleft", _pause=True)
    time.sleep(1)
    pag.typewrite("command Prompt",interval=0.2)
    time.sleep(0.5)
    pag.press("enter")
    time.sleep(4)
    
    pag.typewrite("cd Desktop/koti/koti/tmp/telit/",interval=0.3)
    pag.press("enter")
    time.sleep(3)

    pag.typewrite("processkill.bat",interval=0.3)
    pag.press("enter")
    time.sleep(3)
    
    pag.typewrite("exit",interval=0.3)
    pag.press("enter")
    time.sleep(3)
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
        
    pag.typewrite("./Desktop/iperf-2.1.5-win.exe -s -u -i 1 -t 3000 -p 45679 -l 1400",interval=0.2)
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

    win32gui.CloseWindow(handle_cmd_UL_s_bidi)
    #time.sleep(30)
    #print("Taking screenshot")
    #myScreenshot = pyautogui.screenshot()
    #time.sleep(2)
    #myScreenshot.save(os.path.join(cwd1,"UL_PASS.jpg"))
    #time.sleep(2)
    #time.sleep(100)

    time.sleep(60)
    print("Taking screenshot")
    myScreenshot = pyautogui.screenshot()
    time.sleep(2)
    myScreenshot.save(os.path.join(cwd1,"Bidirectional_Performance.jpg"))
    time.sleep(2)
    time.sleep(60)
    
    #win32gui.CloseWindow(handle_cmd_UL_s_bidi)
    win32gui.CloseWindow(handle_cmd_UL_c_bidi)
    #win32gui.CloseWindow(handle_cmd_UL_s_bidi)


    subprocess.call("taskkill /f /im putty.exe", shell=True)
    subprocess.call("taskkill /f /im powershell.exe", shell=True)
    
    pag.press("winleft", _pause=True)
    time.sleep(1)
    pag.typewrite("command Prompt",interval=0.2)
    time.sleep(0.5)
    pag.press("enter")
    time.sleep(4)
    
    pag.typewrite("cd Desktop/koti/koti/tmp/telit/",interval=0.3)
    pag.press("enter")
    time.sleep(3)

    pag.typewrite("processkill.bat",interval=0.3)
    pag.press("enter")
    time.sleep(3)
    
    pag.typewrite("exit",interval=0.3)
    pag.press("enter")
    time.sleep(3)
    
    
    attach_file = open(file_path,'w')
    attach_file.write("done")
    attach_file.close()




