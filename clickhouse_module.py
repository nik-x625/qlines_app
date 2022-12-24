import clickhouse_connect


client_handler = clickhouse_connect.get_client(
    host='localhost', port='7010', username='default')


def fetch_data_per_param(user_name, client_name, param_name, limit, table_name='table1'):
    res = client_handler.query("SELECT param_name, ts, param_value FROM {} WHERE user_name='{}' and client_name='{}' and param_name='{}' ORDER BY ts DESC LIMIT {}".format(
        table_name, user_name, client_name, param_name, limit))
    return res


def fetch_device_overview(table_name, user_name, limit):
        
    res_temp = client_handler.query("select user_name, client_name, min(ts) as first_message, max(ts) as last_message \
    from {} where user_name='{}' group by client_name, user_name order by last_message desc limit {}"\
        .format(table_name, user_name, limit))
    query_res = res_temp.result_set
    
    print('##### res_temp is: '+str(query_res))
    print('##### res_temp is - type: '+str(type(query_res[0])))
    
    data = []
    for row in query_res:
        data_row = {}
        data_row['user_name'] = row[0]
        data_row['client_name'] = row[1]
        data_row['first_message'] = row[2]
        data_row['last_message'] = row[3]
        
        data.append(data_row)
        
            
    print('# data (db) is: '+str(data))
        
    
    res = {
        'data': data,
        'recordsFiltered': 30,
        'recordsTotal': 230,
    }


    return res
