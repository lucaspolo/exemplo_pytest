import pytest
from validation import cpf_valido


class TestValidation:
    @pytest.mark.parametrize("cpf,expected", [
        ("390.533.447-05", True),
        ("39053344705", True),
        ("123.456.789-09", True),
        ("111.111.111-11", False),
        ("123", False),
        ("", False),
        (None, False),
        (12345678909, False),
    ])
    def test_cpf_valido(self, cpf, expected):
        assert cpf_valido(cpf) is expected