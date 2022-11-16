import pyautogui
import os

lava_job_id="1234"
print(type(lava_job_id))

screenshot_path=(rf"Z:\results\screenshots\{lava_job_id}")
access_rights = 0o755
os.mkdir(screenshot_path, access_rights )
myScreenshot = pyautogui.screenshot()
myScreenshot.save(rf"Z:\results\screenshots\{lava_job_id}\{lava_job_id}.jpg")