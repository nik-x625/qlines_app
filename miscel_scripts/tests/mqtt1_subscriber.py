#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("temp1")

def on_message(client, userdata, msg):
    
    print(str(msg.payload.decode()))
    #if msg.payload.decode() == "Hello world!":
    #    print("Yes!")
    #    client.disconnect()
    
client = mqtt.Client()
client.connect("mqtt.eclipseprojects.io",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()