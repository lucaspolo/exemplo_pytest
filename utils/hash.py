import hashlib


def gerar_id_pessoa(cpf: str, rg: str) -> str:
    """
    Gera um ID único para uma pessoa baseado no CPF e RG.
    
    Args:
        cpf: CPF da pessoa
        rg: RG da pessoa
        
    Returns:
        ID único no formato: {cpf}-{rg}-{hash_md5}
    """
    prefixo = f"{cpf}-{rg}"
    hash_md5 = hashlib.md5(prefixo.encode()).hexdigest()
    id_unico = f"{prefixo}-{hash_md5}"
    return id_unico
