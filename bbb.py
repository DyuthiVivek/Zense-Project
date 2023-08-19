from subprocess import Popen
import time
import os
import signal

p = Popen('/home/dyuthi/Zense-Project/record.py', shell=False)
processId = p.pid
print("Yaya! - Process ID is", processId)
time.sleep(10)
os.kill(processId, signal.SIGINT);
time.sleep(10)
print("Done")
#p.communicate() # to wait until the end
