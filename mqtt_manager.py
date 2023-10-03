#!/usr/bin/env python
from datetime import datetime
import paho.mqtt.client as mqtt
from logger_custom import get_module_logger
logger = get_module_logger(__name__)


MQTT_BROKER_HOST = '127.0.0.1'  # Replace with your broker's hostname or IP
MQTT_BROKER_PORT = 1883  # Replace with your broker's port
MQTT_TOPIC = 'ser_to_cl_topic1'  # Replace with the desired MQTT topic

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f'Connected to MQTT Broker with result code {rc}')
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f'Received message on topic {msg.topic}: {msg.payload.decode()}')
    # Handle the received message here

client.on_connect = on_connect
client.on_message = on_message

def connect_to_mqtt_broker():
    logger.debug('# going to connect')
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    logger.debug('# connected')
    client.loop_start()  # Start the MQTT client loop
    return client
