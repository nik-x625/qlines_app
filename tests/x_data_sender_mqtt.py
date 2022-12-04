import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import numpy as np
import datetime
import json

mqttBroker = "127.0.0.1"
#mqttBroker = "broker.hivemq.com"
#mqttBroker = "mqtt.eclipseprojects.io"


def create_random_data(client_name, param_name, u, sigma):
    ms = datetime.datetime.now()
    now = time.mktime(ms.timetuple())
    s = np.random.normal(u, sigma, 1)
    data = [now, client_name, param_name, s[0]]
    return data


def mqtt_establish():
    client = mqtt.Client('xxx sender')
    client.connect(mqttBroker)
    return client


client = None

while True:

    # Establishing the mqtt connection if not exists
    if not client:
        try:
            client = mqtt_establish()
        except Exception as e:
            print('the initial connection attempt failed')
            time.sleep(1)
            print()
            continue

    try:
        if client._state != 0:
            print('# connection attempt failed, skipping data point...')
            continue
        else:
            data1 = create_random_data('cpe1', 'param1', 20, 5)
            data2 = create_random_data('cpe1', 'param2', 100, 5)
            res1 = client.publish("topic1", json.dumps(data1))
            res2 = client.publish("topic1", json.dumps(data2))
            print('The sending attempt has for data1 result: ', (res1.is_published()),' and data is: ', data1)
            print('The sending attempt has for data1 result: ', (res2.is_published()),' and data is: ', data2)
            #print("Just published " + str(data) + " to broker")
            #print('client obj: '+str(dir(client)))

    except Exception as e:
        print('The error occured: {}, skipping this data point...'.format(e))
        client = None

    print()
    time.sleep(1)
