import time
import numpy as np
import clickhouse_connect
from datetime import datetime

client = clickhouse_connect.get_client(host='localhost', port='7000', username='default')
client.command('CREATE TABLE IF NOT EXISTS table1 (ts DATETIME, client_name String, param_name String, param_value Float64) ENGINE MergeTree ORDER BY client_name')

while(1):
    
    ### cpe1
    ### param1
    client_name = 'cpe1'
    param_name = 'param1'
    now = datetime.now()
    s = np.random.normal(10, 1, 1)
    param_dict = [now, client_name, param_name, s[0]] #{'param1':s[0]}
    client.insert('table1', [param_dict], column_names=['ts', 'client_name', 'param_name', 'param_value'])
    print('# data to write for cpe1 - param 1: '+str(s[0]))

    ### param2
    client_name = 'cpe1'
    param_name = 'param2'
    now = datetime.now()
    s = np.random.normal(100, 1, 1)
    param_dict = [now, client_name, param_name, s[0]] #{'param1':s[0]}
    client.insert('table1', [param_dict], column_names=['ts', 'client_name', 'param_name', 'param_value'])
    print('# data to write for cpe1 - param 2: '+str(s[0]))
    
    
    ### cpe2
    ### param1
    client_name = 'cpe2'
    param_name = 'param1'
    now = datetime.now()
    s = np.random.normal(20, 1, 1)
    param_dict = [now, client_name, param_name, s[0]] #{'param1':s[0]}
    client.insert('table1', [param_dict], column_names=['ts', 'client_name', 'param_name', 'param_value'])
    print('# data to write for cpe2 - param 1: '+str(s[0]))
    
    ### cpe2
    ### param2
    client_name = 'cpe2'
    param_name = 'param2'
    now = datetime.now()
    s = np.random.normal(200, 1, 1)
    param_dict = [now, client_name, param_name, s[0]] #{'param1':s[0]}
    client.insert('table1', [param_dict], column_names=['ts', 'client_name', 'param_name', 'param_value'])
    print('# data to write for cpe2 - param 2: '+str(s[0]))


    print()
    time.sleep(1)