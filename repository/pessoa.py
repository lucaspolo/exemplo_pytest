from typing import Dict, Any
from psycopg2.extras import Json
from repository import pessoa_sql
from utils.hash import gerar_id_pessoa


class PessoaRepository:
    def __init__(self, conn):
        self.conn = conn


    def inserir_pessoa(self, data: Dict[str, Any]) -> str:
        # Validar campos obrigatórios para geração do ID
        if not data.get("cpf"):
            raise ValueError("Campo obrigatório ausente: 'cpf'.")
        if not data.get("rg"):
            raise ValueError("Campo obrigatório ausente: 'rg'.")

        # Gerar ID único baseado em CPF e RG
        cpf = data.get("cpf")
        rg = data.get("rg")
        id_unico = gerar_id_pessoa(cpf, rg)

        params = {
            "id": id_unico,
            "nome": data.get("nome"),
            "cpf": cpf,
            "rg": rg,
            "data_nascimento": data.get("data_nascimento"),
            "telefones": Json(data.get("telefones")) if data.get("telefones") is not None else None,
        }

        sql = pessoa_sql.INSERT_PESSOA

        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()[0]

    def buscar_pessoa(self, pessoa_id: str) -> Dict[str, Any]:
        """Busca uma pessoa pelo ID"""
        sql = pessoa_sql.SELECT_PESSOA_BY_ID
        
        with self.conn.cursor() as cur:
            cur.execute(sql, (pessoa_id,))
            row = cur.fetchone()
            
            if row:
                return {
                    "id": row[0],
                    "nome": row[1],
                    "cpf": row[2],
                    "rg": row[3],
                    "data_nascimento": row[4],
                    "telefones": row[5]
                }
            return None

    def listar_pessoas(self) -> list[Dict[str, Any]]:
        """Lista todas as pessoas"""
        sql = pessoa_sql.SELECT_ALL_PESSOAS
        
        with self.conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            
            return [
                {
                    "id": row[0],
                    "nome": row[1],
                    "cpf": row[2],
                    "rg": row[3],
                    "data_nascimento": row[4],
                    "telefones": row[5]
                }
                for row in rows
            ]

    def deletar_pessoa(self, pessoa_id: str) -> bool:
        """Deleta uma pessoa pelo ID"""
        sql = pessoa_sql.DELETE_PESSOA_BY_ID
        
        with self.conn.cursor() as cur:
            cur.execute(sql, (pessoa_id,))
            return cur.rowcount > 0    
