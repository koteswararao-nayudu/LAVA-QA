from pathlib import Path
import os

#windows_results_file_path = 'Z:\\lava-qa\\results\\windows-results\\cell_attach.txt'
#linux_results_file_path = 'Z:\\lava-qa\\results\\linux-results\\cell_up_status.txt'

if os.path.exists(windows_results_file_path):
    os.remove(windows_results_file_path)
    print("file is there")
else:
    print("no file")

if os.path.exists(linux_results_file_path): 
    os.remove(linux_results_file_path)
    print("file is there")
else:
    print("no file")
    