# Teste com Pytest - Unitários e Integrados

Para executar esta aplicação é necessário:
- Python 3.11
- Poetry 1.8
- docker compose

Recomendo ter o `mise` instalado na máquina, ele ajuda a versionar o Python e o Poetry, se tiver instalado rode no diretório raiz desse projeto:

```
mise use python@3.11 poetry@1.8
```

Ele irá instalar para vc ambos e neste diretório sempre ativará estas versões =)

## Configurando

Inicie o Poetry Shell e execute a instalação:

```
poetry shell
poetry install
```

Suba os containers:

```
docker compose up -d
```

Rode as migrations:

```
yoyo apply
```

E execute o main.py:

```
python main.py
```

Com isto a aplicação já está executando, você pode enviar via AKHQ para o `input-topic` a seguinte mensagem:

```
{
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
      "ramal": null,
      "whatsapp": true,
      "principal": true
    }
  ]
}
```

Caso de tudo certo, você deverá ver uma mensagem no `output-topic`