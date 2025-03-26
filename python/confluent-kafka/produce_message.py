#!/usr/bin/env python3

from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': 'localhost:9092',
        'client.id': socket.gethostname()}

producer = Producer(conf)

topic = "quickstart-events"

producer.produce(topic, key="key", value="value")
producer.flush()
