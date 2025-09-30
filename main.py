from datetime import datetime, timezone
from decimal import Decimal

import psycopg2

from repository.pessoa import PessoaRepository
from config import DSN


def main():   
    with psycopg2.connect(DSN) as conn:  
        pessoa_repository = PessoaRepository(conn)

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
        print(pessoa_repository.listar_pessoas())


if __name__ == "__main__":
    main()
