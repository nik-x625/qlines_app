import psutil

def check_process_cmdline(process_name, expected_cmdline):
    for proc in psutil.process_iter(['name', 'cmdline']):
        
        #print('# going through processes: '+str(proc.info['name'] + '        ' + ' '.join(proc.info['cmdline'])))
        
        if proc.info['name'] == process_name:
            actual_cmdline = ' '.join(proc.info['cmdline'])
            #print('# found the name: '+str(proc.info['name']))
            #print('# found the cmd: '+str(actual_cmdline))
            
            #if proc.info['name'] == 'java':
            #    print(' '.join(proc.info['cmdline']))
            #    if ' '.join(proc.info['cmdline']
            if (expected_cmdline.strip() in actual_cmdline.strip()):
                return (True, '')
            else:
                
                print('# expected_cmdline: '+str(expected_cmdline))
                print('# actual_cmdline: '+str(actual_cmdline))
                return (False, actual_cmdline.strip())
            
    return False, ''
                

        
        
    return False

if __name__ == "__main__":
    # List of dictionaries containing process names and expected command lines
    process_list = [
        {"title":"rqworker", "name": "python", "cmdline": 'python /opt/qlines_app/rqworker.py'},
        {"title":"mongodb", "name": "mongod", "cmdline": "/usr/bin/mongod --config /etc/mongod.conf"},
        {"title":"mosquitto", "name": "mosquitto", "cmdline": "/usr/sbin/mosquitto -d"},
        {"title":"clickhouse-server", "name": "clickhouse-server", "cmdline": "clickhouse-server --config-file /etc/clickhouse-server/config.xml --pid-file /var/run/clickhouse-server/clickhouse-server.pid --daemon"},
        {"title":"clickhouse-watchd", "name": "clckhouse-watch", "cmdline": "clickhouse-watchd --config-file /etc/clickhouse-server/config.xml --pid-file /var/run/clickhouse-server/clickhouse-server.pid --daemon"},
        {"title":"redis", "name": "redis-server", "cmdline": "/usr/bin/redis-server 127.0.0.1:6379"},
        {"title":"kafka", "name": "java", "cmdline": "XX:+UseG1GC"},
        {"title":"gunicorn", "name": "gunicorn", "cmdline": "--worker-class eventlet -w 1"},
        
        #{"title":"kafka", "name": "java", "cmdline": "-Xmx1G -Xms1G -server -XX:+UseG1GC -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35"},
        # Add more processes and expected command lines as needed
        # redis-server kafka rqworker gunicorn
    ]

    for process_info in process_list:
        process_name = process_info["name"]
        process_title = process_info["title"]
        expected_cmdline = process_info["cmdline"]
        #res = check_process_cmdline(process_name, expected_cmdline)
        #print('res is: '+str(res))
        
        #print()
        #print('going to check process: '+str(process_name))
        is_running, actual_command = check_process_cmdline(process_name, expected_cmdline)

        if is_running:
            print(f"Process '{process_title}' is OK and running") # with CMD: {expected_cmdline}")
        else:
            print(f"Process '{process_title}' --- is NOT OK and NOT running or the CMD doesn't match the expected value. Actual command is: "+str(actual_command))
