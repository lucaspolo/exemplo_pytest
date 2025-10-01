from enum import auto
from locale import normalize
import pathlib
import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import RedpandaContainer
from yoyo import get_backend, read_migrations

POSTGRES_IMAGE = "postgres:18"  # versão fixada
REDPANDA_IMAGE = "redpandadata/redpanda:v25.2.6" 
MIGRATIONS_DIR = pathlib.Path(__file__).parent.parent / "migrations"


@pytest.fixture(scope="session", autouse=True)
def pg_url():
    # Sobe o container apenas uma vez por sessão de testes
    with PostgresContainer(POSTGRES_IMAGE) as pg:
        yield pg.get_connection_url()  # e.g. postgresql+psycopg2://user:pass@host:port/db


def _normalize_pg_url(sa_url: str) -> str:
    # yoyo espera DSN estilo "postgresql://", enquanto o testcontainers retorna
    # "postgresql+psycopg2://". Removemos o driver.
    return sa_url.replace("postgresql+psycopg2://", "postgresql://")


@pytest.fixture(scope="session", autouse=True)
def _apply_migrations(pg_url):
    """
    Aplica todas as migrações do yoyo no início da sessão.
    Faz rollback ao final da sessão (pode desligar com ROLLBACK_MIGRATIONS_AT_END=0).
    """
    dsn = _normalize_pg_url(pg_url)
    backend = get_backend(dsn)
    migrations = read_migrations(str(MIGRATIONS_DIR))

    # Aplica migrações que faltam
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

    yield


@pytest.fixture
def db_conn(pg_url):
    conn = psycopg2.connect(_normalize_pg_url(pg_url))
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture(scope="session")
def kafka_bootstrap():
    # Sobe o Kafka num container e retorna o bootstrap servers
    with RedpandaContainer(REDPANDA_IMAGE) as redpanda:
        bs = redpanda.get_bootstrap_server()        
        yield bs
