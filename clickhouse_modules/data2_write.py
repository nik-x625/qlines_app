import time
import numpy as np
import clickhouse_connect
from datetime import datetime

client = clickhouse_connect.get_client(host='localhost', port='7010', username='default')
client.command('CREATE TABLE IF NOT EXISTS table1 (ts DATETIME, client_name String, param_name String, param_value Float64) ENGINE MergeTree ORDER BY client_name')

def write_random_data(client_name, param_name):
    now = datetime.now()
    s = np.random.normal(10, 1, 1)
    param_dict = [now, client_name, param_name, s[0]]
    client.insert('table1', [param_dict], column_names=['ts', 'client_name', 'param_name', 'param_value'])
    print('# data to write for {} - {}: {}'.format(client_name, param_name, s[0]))
    
while(1):
    write_random_data('cpe1', 'param1')
    
    print()
    time.sleep(5)