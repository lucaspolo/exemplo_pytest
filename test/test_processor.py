
from unittest import mock
from unittest.mock import MagicMock
import pytest
from messaging import create_consumer, create_producer
import config
from processor import Processor
from repository.pessoa import PessoaRepository


def test_processor_should_recieve_message_and_persist():
    db_conn = MagicMock()
    message = MagicMock()
    message.value = {
        "nome": "Maria Clara dos Santos",
        "cpf": "123.456.789-09",
        "rg": "12.345.678-9",
        "data_de_nascimento": "1990-05-17",
        "telefones": [
            {
                "tipo": "celular",
                "ddi": "+55",
                "ddd": "21",
                "numero": "99876-5432",
                "ramal": None,
                "whatsapp": True,
                "principal": True,
            },
        ],
    }
    consumer = [message]

    with mock.patch("processor.PessoaRepository") as MockPessoaRepository:
        mock_repo_instance = MockPessoaRepository.return_value
        mock_repo_instance.inserir_pessoa = MagicMock()
        processor = Processor(
            db_conn=db_conn,
            consumer=consumer,
            max_messages=1,
        )

        processor.start()

        assert mock_repo_instance.inserir_pessoa.call_count == 1
        mock_repo_instance.inserir_pessoa.assert_called_with(message.value)


# =================== TESTES INTEGRADOS ========================

@pytest.fixture
def producer_to_input(kafka_bootstrap):
    settings = config.PRODUCER_CONFIG.copy()
    settings["bootstrap_servers"] = kafka_bootstrap
    return create_producer(
        settings,
    )

@pytest.fixture
def consumer(kafka_bootstrap):
    settings = config.CONSUMER_CONFIG.copy()
    settings["bootstrap_servers"] = kafka_bootstrap
    settings["group_id"] = "test-group-input"  # Group ID único para testes
    settings["consumer_timeout_ms"] = 1000  # Timeout de 1 segundo
    return create_consumer(
        "input_test_topic",
        settings,
    )

@pytest.fixture
def producer(kafka_bootstrap):
    settings = config.PRODUCER_CONFIG.copy()
    settings["bootstrap_servers"] = kafka_bootstrap
    return create_producer(
        settings,
    )

@pytest.fixture
def consumer_from_output(kafka_bootstrap):
    settings = config.CONSUMER_CONFIG.copy()
    settings["bootstrap_servers"] = kafka_bootstrap
    settings["group_id"] = "test-group-output"  # Group ID único para testes
    settings["consumer_timeout_ms"] = 1000  # Timeout de 1 segundo
    return create_consumer(
        "output_test_topic",
        settings,
    )



@pytest.fixture
def pessoa_repository(db_conn):
    return PessoaRepository(db_conn)

    
def test_processor_should_persist_data(
        db_conn, consumer, producer_to_input, pessoa_repository
):
    processor = Processor(
        db_conn=db_conn,
        consumer=consumer,
        max_messages=1,
    )

    producer_to_input.send(
        "input_test_topic",
        value= {
            "nome": "Maria Clara dos Santos",
            "cpf": "123.456.789-09",
            "rg": "12.345.678-9",
            "data_de_nascimento": "1990-05-17",
            "telefones": [
                {
                    "tipo": "celular",
                    "ddi": "+55",
                    "ddd": "21",
                    "numero": "99876-5432",
                    "ramal": None,
                    "whatsapp": True,
                    "principal": True,
                },
            ],
        }
    )

    processor.start()
    pessoas = pessoa_repository.listar_pessoas()
    assert len(pessoas) == 1


def test_processor_should_produce_in_output_topic(
    db_conn, consumer, producer_to_input, producer, consumer_from_output
):
    processor = Processor(
        db_conn=db_conn,
        consumer=consumer,
        producer=producer,
        producer_topic="output_test_topic",
        max_messages=1,
    )

    producer_to_input.send(
        "input_test_topic",
        value= {
            "nome": "Maria Clara dos Santos",
            "cpf": "123.456.789-09",
            "rg": "12.345.678-9",
            "data_de_nascimento": "1990-05-17",
            "telefones": [
                {
                    "tipo": "celular",
                    "ddi": "+55",
                    "ddd": "21",
                    "numero": "99876-5432",
                    "ramal": None,
                    "whatsapp": True,
                    "principal": True,
                },
            ],
        }
    )
    producer_to_input.flush()  # Garante que a mensagem seja enviada

    processor.start()

    # Adiciona timeout para evitar travamento
    import time
    timeout = time.time() + 1  # 1 segundo de timeout
    
    try:
        for msg in consumer_from_output:
            if time.time() > timeout:
                pytest.fail("Timeout: Nenhuma mensagem recebida em 1 segundo")
            
            data = msg.value
            assert data["cpf_valido"] is False
            assert "persisted_at" in data
            break
    except StopIteration:
        pytest.fail("Nenhuma mensagem foi recebida no tópico de output")