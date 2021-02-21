import psutil
import time
x = psutil.cpu_times_percent(interval=.2)

#time.sleep(0.5)
#x = psutil.cpu_times_percent()
print(x.user)