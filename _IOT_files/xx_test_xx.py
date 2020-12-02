'''
import subprocess
#subprocess.Popen("cat asterisk_stop.txt | ssh root@127.0.0.1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#subprocess.Popen("cat asterisk_start.txt | ssh root@127.0.0.1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()



        #subprocess.check_output(my_command, shell=True, stderr=subprocess.STDOUT)

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()

'''

from flask import Flask
import subprocess
app = Flask(__name__)

@app.route('/')
def hello_world():
    cmd = "cat /var/www/site_iot/asterisk_stop.txt | ssh root@127.0.0.1"
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return 'Hello, World!'


app.run(host='0.0.0.0', port=8585, debug=True)
