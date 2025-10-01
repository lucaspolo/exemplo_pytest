from datetime import datetime
from venv import create

from kafka import KafkaConsumer, KafkaProducer
import psycopg2
from messaging import create_consumer
from repository.pessoa import PessoaRepository
from test.conftest import kafka_bootstrap

import config


class Processor:
    def __init__(
            self, 
            db_conn: psycopg2.extensions.connection, 
            consumer: KafkaConsumer, 
            producer: KafkaProducer,
            producer_topic: str = config.KAFKA_PRODUCER_TOPIC
    ):
        self.db_conn = db_conn
        self.consumer = consumer
        self.producer = producer
        self.pessoa_repository = PessoaRepository(self.db_conn)
        self.producer_topic = producer_topic

    def start(self):
        for msg in self.consumer:
            data = msg.value
            print(f"Mensagem recebida: {data}")
            self.pessoa_repository.inserir_pessoa(data)
            data["persisted_at"] = datetime.now().isoformat()
            self.producer.send(self.producer_topic, value=data)