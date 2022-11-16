import serial
import time

ser = serial.Serial(port="COM11", baudrate=115200, bytesize=8, stopbits=serial.STOPBITS_ONE)

#ser = serial.Serial(port, 9600, timeout=1)
#ser.close()
#ser.open()
ser.write(b"at \r\n")
time.sleep(3)
read_val = ser.readline()
strip_read_data=read_val.strip().decode( "utf-8" )
print(strip_read_data)

#serialString = ""
#serialPort.flushInput()
#serialPort.flushOutput()
##serialPort.write("at")
#serialPort.write(b"at \r\n")

#time.sleep(.1)
##serialPort.flush()
##serialPort.flushInput()
#time.sleep(.1)
##read_data = serialPort.readline()
#read_data = serialPort.read_line()
#strip_read_data=read_data.strip().decode( "utf-8" )
#print("##################")
#print(strip_read_data)
#print("##################")s

#serialString = serialPort.readline()
#print(serialString.decode("Ascii"))

# if serialPort.in_waiting > 0:
    # print("we are in serial port print section")
    # serialString = serialPort.readline()
    # try:
        # print(serialString.decode("Ascii"))
    # except:
        # OK
        
# def write_read(x):
    # serialPort.write(b"at \r\n")
    # time.sleep(0.05)
    # data = serialPort.read_line()
    # return data
# while True:
    # num = input("Enter a number: ") # Taking input from user
    # value = write_read(num)
    # print(value) # printing the value
    
