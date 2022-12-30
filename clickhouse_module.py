import clickhouse_connect
from logger_custom import get_module_logger
from datetime_converter import datetime_to_elapsed

# for timezone management, ref: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-dates-and-times
from momentjs import momentjs
#from qlines import app
#app.jinja_env.globals['momentjs'] = momentjs


logger = get_module_logger(__name__)


client_handler = clickhouse_connect.get_client(
    host='localhost', port='7010', username='default', query_limit=0)


def fetch_data_per_param(user_name, client_name, param_name, limit, table_name='table1'):
    res = client_handler.query("SELECT param_name, ts, param_value FROM {} WHERE user_name='{}' and client_name='{}' and param_name='{}' ORDER BY ts DESC LIMIT {}".format(
        table_name, user_name, client_name, param_name, limit))
    return res


def fetch_device_overview(table_name, user_name, like, start, length, order):

    order_by = order[0]['column_name']
    order_direction = order[0]['direction']

    # to get the number for 'recordsTotal'
    res_total = client_handler.query(
        "select count(distinct(client_name)) from table1 where user_name='{}'".format(user_name))
    recordsTotal = res_total.result_set

    # to do the main query to get the filtered data
    # res_filtered = client_handler.query("select count(*) OVER () AS TotalRecords, user_name, client_name, min(ts) as first_message, max(ts) as last_message \
    # from {} where user_name='{}' and (client_name like '%{}%' OR user_name like '%{}%') group by client_name, user_name order by {} {} offset {} rows fetch next {} rows only"
    #                                    .format(table_name, user_name, like, like, order_by, order_direction, start, length))

    # to do the main query to get the filtered data
    query_string = f"select count(*) OVER () AS TotalRecords, user_name, client_name, min(ts) \
as first_message, max(ts) as last_message from {table_name} where \
user_name='{user_name}' and (client_name like '%{like}%' \
OR user_name like '%{like}%') group by client_name, user_name \
order by {order_by} {order_direction} \
offset {start} rows fetch next {length} rows only"

    res_filtered = client_handler.query(query_string)
    query_res = res_filtered.result_set

    data = []
    count = 0
    for row in query_res:
        data_row = {}
        data_row['user_name'] = row[1]
        data_row['client_name'] = row[2]
        # + ' - ' + datetime_to_elapsed(row[3])
        data_row['first_message'] = (row[3])
        # + ' - ' + datetime_to_elapsed(row[4])
        data_row['last_message'] = row[4]

        count = row[0]

        data.append(data_row)

    # print('# data (db) is: '+str(data))

    res = {
        'data': data,
        'recordsFiltered': count,  # recordsFiltered[0][0],
        'recordsTotal': recordsTotal[0][0],
    }

    return res


if __name__ == '__main__':
    res = fetch_device_overview('table1', 'a@b.c', 'cpe2', 10)
    res1 = res.result_set

    print('res is: '+str(res1))

    ''' 
    clickhouse cli direct command here:
    
    select user_name, client_name, min(ts) as first_message, max(ts) as last_message from table1 where user_name='a@b.c' and client_name like '%cpe%' group by client_name, user_name order by last_message desc limit 20
    
    '''
