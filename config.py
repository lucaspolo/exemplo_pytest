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
