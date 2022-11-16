from pathlib import Path
import os
import time

linux_results_file_path = 'Z:\\lava-qa\\results\\linux-results\\cell_up_status.txt'
windows_results_file_path = 'Z:\\lava-qa\\results\\windows-results\\cell_attach.txt'

print("Waiting for CELL UP")

flag=False
while [ True ]:
    if os.path.exists(linux_results_file_path):
        f = open(linux_results_file_path, "r")
        string1="done"
        print(string1)
        time.sleep(2)
        if string1 in f.read():
            flag=True
            print("CELL UP Done")
            break;
            
    if [ flag == True ]:
        break

#print("Waiting for CELL UP")
#while [ True ]:
#    if os.path.exists(linux_results_file_path):
#        f = open(linux_results_file_path, "r")
#        time.sleep(2)
#        if Done in f.read():
#            print("CELL UP Done")
#            break