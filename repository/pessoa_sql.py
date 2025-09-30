# SQL queries for pessoa repository

INSERT_PESSOA = """
    INSERT INTO public.pessoas
        (id, nome, cpf, rg, data_nascimento, telefones)
    VALUES
        (%(id)s, %(nome)s, %(cpf)s, %(rg)s, %(data_nascimento)s, %(telefones)s)
    ON CONFLICT (id) DO UPDATE SET
        nome = EXCLUDED.nome,
        cpf = EXCLUDED.cpf,
        rg = EXCLUDED.rg,
        data_nascimento = EXCLUDED.data_nascimento,
        telefones = EXCLUDED.telefones
    RETURNING id;
"""

SELECT_PESSOA_BY_ID = """
    SELECT id, nome, cpf, rg, data_nascimento, telefones
    FROM public.pessoas
    WHERE id = %s
"""

SELECT_ALL_PESSOAS = """
    SELECT id, nome, cpf, rg, data_nascimento, telefones
    FROM public.pessoas
    ORDER BY nome
"""

DELETE_PESSOA_BY_ID = """
    DELETE FROM public.pessoas WHERE id = %s
"""
