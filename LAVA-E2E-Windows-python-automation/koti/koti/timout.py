import time

timeout = 30   # [seconds]

print("#################")
timeout_start = time.time()
print("1st")
print(timeout_start)
print("#################")
print("#################")
print("2nd");
print(time.time())
print("#################")
flag1="true"
flag2="frue"
while [ True ]:
    print("1")
    
    if  flag1 == flag2:
        break
       
    if time.time() > timeout_start + timeout:
        print("timeouot before exit")
        print(time.time())
        time.sleep(0.5)
        exit()


print("hai how are you")