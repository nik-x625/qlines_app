#!/usr/bin/python
'''
module doc bla bla
'''
import time
import datetime
import json
import sys
import getopt
import paho.mqtt.client as mqtt
import numpy as np


mqttBroker = "127.0.0.1"
#mqttBroker = "broker.hivemq.com"
#mqttBroker = "mqtt.eclipseprojects.io"


def rpc_sender(mqtt_rpc_handler, topic, rpc_method, rpc_args):
    rpc_envelop = {'rpc_method': rpc_method,
                   'rpc_args': rpc_args}
    res1 = mqtt_rpc_handler.publish(topic, json.dumps(rpc_envelop))


if __name__ == '__main__':
    # the command sender is the central qlines, command will be sent to the remote client

    mqtt_rpc_handler = None

    try:
        clientname = 'some_client_name'
        mqtt_rpc_handler = mqtt.Client(clientname)
        mqtt_rpc_handler.connect(mqttBroker)

    except Exception as e:
        print('# the rpc mqtt except: '+str(e))

    topic = 'topic-rpc-client1'
    rpc_method = 'spv'
    rpc_args = "{'param1':'val1'}"

    rpc_sender(mqtt_rpc_handler, topic, rpc_method, rpc_args)
