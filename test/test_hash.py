from utils.hash import gerar_id_pessoa


def test_gerar_id_pessoa_should_hash_value():
    value = "teste"
    hashed_value = gerar_id_pessoa("12345678900", "MG1234567")
    assert hashed_value == "12345678900-MG1234567-b3093f315d74b62320e7a41b94b26e3f"  # Valor esperado do hash


def test_gerar_id_pessoa_should_return_md5_digest_from_the_concatened_values():
    cpf = "12345678900"
    rg = "MG1234567"
    expected_prefix = f"{cpf}-{rg}"
    expected_hash = "b3093f315d74b62320e7a41b94b26e3f"  # MD5 de "12345678900-MG1234567"
    expected_id = f"{expected_prefix}-{expected_hash}"
    
    generated_id = gerar_id_pessoa(cpf, rg)
    
    assert generated_id == expected_id