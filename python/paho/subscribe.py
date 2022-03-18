#!/usr/bin/env python3

# https://pypi.org/project/paho-mqtt/#id2
# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4

import paho.mqtt.client as mqtt
import time

client_name = "client2"
mqtt_broker = "localhost"
#mqtt_broker = "mqtt.eclipseprojects.io"
topic = "test"

# The callback for when the client receives a CONNACK response from the server.
# Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, message):
    print(f"Received message on { message.topic }: { message.payload.decode('utf-8') }")

client = mqtt.Client(client_name)
client.on_connect = on_connect
client.on_message = on_message 

client.connect(mqtt_broker)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
client.loop_forever()