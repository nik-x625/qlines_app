#!/usr/bin/env python
from datetime import datetime
import paho.mqtt.client as mqtt
from logger_custom import get_module_logger

import json
import time
import clickhouse_connect
from datetime import datetime
import paho.mqtt.client as mqtt
import threading
logger = get_module_logger(__name__)


dbclient = clickhouse_connect.get_client(
    host='localhost', port='7010', username='default')

dbclient.command(
    'CREATE TABLE IF NOT EXISTS table1 (ts DATETIME, user_name String, client_name String, param_name String, param_value Float64) ENGINE MergeTree ORDER BY client_name')


MQTT_BROKER_HOST = '127.0.0.1'  # Replace with your broker's hostname or IP
MQTT_BROKER_PORT = 1883  # Replace with your broker's port
MQTT_TOPIC = 'ser_to_cl_topic1'  # Replace with the desired MQTT topic

client = mqtt.Client()

# def on_connect(client, userdata, flags, rc):
#     print(f'Connected to MQTT Broker with result code {rc}')
#     client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):

    print('# in on_message function')

    data = []

    # print('# mqtt received: ', msg.payload)
    print('# mqtt received: ', msg.payload.decode())
    # print('# mqtt received - type: ', type(msg.payload.decode()))

    try:
        data = msg.payload.decode()
        data = json.loads(data)
        data[0] = datetime.fromtimestamp(data[0])

        print('# going to update db with: ', data)

        dbclient.insert('table1', [data], column_names=[
            'ts', 'user_name', 'client_name', 'param_name', 'param_value'])
        print()

    except Exception as e:
        print('# error in processing the recevied mqtt message: ', e)


client = mqtt.Client('receiver_clickhouse')
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)

# client.on_connect = on_connect
client.on_message = on_message
client.subscribe("us_topic_for_all")

# client.loop_start()


def mqtt_loop():
    client.loop_forever()


mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.start()


def connect_to_mqtt_broker():
    logger.debug('# in the function connect_to_mqtt_broker')
    # client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    # logger.debug('# connected')
    # client.loop_start()  # Start the MQTT client loop
    return client
