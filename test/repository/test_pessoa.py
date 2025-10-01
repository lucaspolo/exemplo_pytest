import pytest
from repository.pessoa import PessoaRepository

class TestPessoaRepository:
    @pytest.fixture
    def pessoa_repository(self, db_conn):
        return PessoaRepository(db_conn)

    def test_criar_pessoa(self, pessoa_repository, kafka_bootstrap):
        data = {
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

        pessoa_repository.inserir_pessoa(data)
        assert len(pessoa_repository.listar_pessoas()) == 1