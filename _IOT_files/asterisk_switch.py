#!/usr/bin/python
import subprocess
print('# inside asterisk_switch')
#subprocess.Popen("cat /var/www/site_iot/asterisk_stop.txt | ssh root@127.0.0.1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#subprocess.Popen("cat asterisk_start.txt | ssh root@127.0.0.1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def switch():
       #res = subprocess.Popen("pwd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
       #return res
       result = subprocess.Popen("cat /var/www/site_iot/asterisk_stop.txt | ssh root@127.0.0.1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
       res = [result.returncode, result.stdout, result.stderr]
       
       return res