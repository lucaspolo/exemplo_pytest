import json
from kafka import KafkaConsumer, KafkaProducer

import config


def create_consumer(consumer_topic = None, settings = None) -> KafkaConsumer:
    if not consumer_topic:
        consumer_topic = config.KAFKA_CONSUMER_TOPIC
    if not settings:
        settings = config.CONSUMER_CONFIG
    
    consumer = KafkaConsumer(
        consumer_topic, 
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
        key_deserializer=lambda b: b.decode("utf-8") if b is not None else None,
        **settings
    )

    return consumer


def create_producer(settings = None):
    if not settings:
        settings = config.PRODUCER_CONFIG

    producer = KafkaProducer(
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda v: v.encode("utf-8") if v is not None else None,
        **settings
    )

    return producer