#!/usr/bin/env python3

# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4
# https://pypi.org/project/paho-mqtt/#id2

import paho.mqtt.client as mqtt 

mqtt_broker = "localhost"
client_name = "client1"

client = mqtt.Client(client_name)
client.connect(mqtt_broker)

topic = "test"
msg = "Hello from Python!"
client.publish(topic, payload=msg)
#client.publish(topic, payload=msg, qos=0, retain=False)