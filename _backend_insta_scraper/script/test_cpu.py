import psutil
p = psutil.Process()
print p.cpu_percent(interval=1)
print p.cpu_percent(interval=None)