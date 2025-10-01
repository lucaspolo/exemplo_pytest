from datetime import datetime
from email import message
from venv import create

from kafka import KafkaConsumer, KafkaProducer
import psycopg2
from messaging import create_consumer
from repository.pessoa import PessoaRepository
from test.conftest import kafka_bootstrap

import config
from validation import cpf_valido


class Processor:
    def __init__(
            self, 
            db_conn: psycopg2.extensions.connection, 
            consumer: KafkaConsumer, 
            producer: KafkaProducer = None,
            producer_topic: str = config.KAFKA_PRODUCER_TOPIC,
            max_messages: int = None,
    ):
        self.db_conn = db_conn
        self.consumer = consumer
        self.producer = producer
        self.pessoa_repository = PessoaRepository(self.db_conn)
        self.producer_topic = producer_topic
        self.max_messages = max_messages

    def start(self):
        message_count = 0
        for msg in self.consumer:
            data = msg.value
            data = self.process(data)
            if self.producer:
                self.producer.send(self.producer_topic, value=data)
                self.producer.flush()  # Garante que a mensagem seja enviada
            message_count += 1
            if self.max_messages and message_count >= self.max_messages:
                break

    def process(self, data: dict) -> dict:
        print(f"Mensagem recebida: {data}")
        self.pessoa_repository.inserir_pessoa(data)
        data["cpf_valido"] = cpf_valido(data)
        data["persisted_at"] = datetime.now().isoformat()
        return data