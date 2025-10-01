from datetime import datetime, timezone
from decimal import Decimal
from multiprocessing import process
import sys

import psycopg2

from messaging import create_consumer, create_producer
from processor import Processor
from repository.pessoa import PessoaRepository
from config import DSN


def main():   
    # with psycopg2.connect(DSN) as conn:
    # ContextManager é melhor, 
    # mas aqui como está criando vários recursos, preferi o try/finally
    try:
        conn = psycopg2.connect(DSN)
        consumer = create_consumer()
        producer = create_producer()

        processor = Processor(conn, consumer, producer)
        processor.start()
    except KeyboardInterrupt:
        print("Finalizando a aplicação, tchaaaaaaaaaaaaaaau!")
        sys.exit(0)
    finally:
        conn.close()
        try:
            producer.flush(10)
        except Exception:
            pass
        producer.close(5)
        consumer.close()


if __name__ == "__main__":
    main()
