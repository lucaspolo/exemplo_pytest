import os

# Configurações do banco de dados
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": os.getenv("DB_PORT", "15432"),
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}

# String de conexão
DSN = "host={host} port={port} dbname={database} user={user} password={password}".format(**DATABASE_CONFIG)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_CONSUMER_TOPIC = "input-topic"
KAFKA_GROUP_ID = "test-group"
KAFKA_PRODUCER_TOPIC = "output-topic"

# Consumer configuration
CONSUMER_CONFIG = {
    "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
    "auto_offset_reset": "earliest",
    "enable_auto_commit": True,
    "group_id": KAFKA_GROUP_ID
}

# Producer configuration
PRODUCER_CONFIG = {
    "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS
}