import os
import subprocess

#os.system('cmd /k "C:\Users\DELL\Desktop\koti\koti\tmp\telit\serial_port_names.bat"')
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


if os.path.exists("C:/Users/DELL/Desktop/koti/koti/tmp/telit/ipaddress_file.txt"):
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
print(output)
clean_line = output_telit_ipaddress.strip().decode( "utf-8" )
print(clean_line)
print("Command exit status/return code : ", telit_ipaddress_status)

if telit_ipaddress_status :
    print("test fail")
else:
    print("test pass")