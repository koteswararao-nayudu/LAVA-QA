import serial
import time
import os
import subprocess


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

#com_string_strip="COM11"
port = serial.Serial(com_string_strip, baudrate=115200, timeout=3.0)



port.write(b"at \r\n")
port.flush()
rcv1 = port.read(20)
rcv1_strip=rcv1.strip().decode( "utf-8" )
print(repr(rcv1_strip))
port.write(b"at+cfun=0 \r\n")
rcv2 = port.read(80)
rcv2_strip=rcv2.strip().decode( "utf-8" )
print(repr(rcv2_strip))
port.write(b"at \r\n")
rcv3 = port.read(80)
rcv3_strip=rcv3.strip().decode( "utf-8" )
print(repr(rcv2_strip))
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


# #while True:
# port.write(b"at \r\n")
# port.flush()
# rcv1 = port.read(20)
# rcv1_strip=rcv1.strip().decode( "utf-8" )
# print(repr(rcv1_strip))
# time.sleep(1)
# port.write(b"at+cfun=0 \r\n")
# rcv2 = port.read(20)
# rcv2_strip=rcv2.strip().decode( "utf-8" )
# print(repr(rcv2_strip))
# port.write(b"at+cfun=1 \r\n")
# time.sleep(2)
# rcv3 = port.read(22)
# rcv3_strip=rcv3.strip().decode( "utf-8" )
# print(repr(rcv3_strip))