
import re

PATTERN_REMOVE_DIGITS = re.compile(r"\D")

def cpf_valido(cpf: str) -> bool:
    if not isinstance(cpf, str):
        return False

    digs = PATTERN_REMOVE_DIGITS.sub("", cpf)
    if len(digs) != 11:
        return False
    if digs == digs[0] * 11:
        return False

    def calc_dv(numeros: str, peso_inicial: int) -> int:
        soma = sum(int(d) * p for d, p in zip(numeros, range(peso_inicial, 1, -1)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    dv1 = calc_dv(digs[:9], 10)
    dv2 = calc_dv(digs[:9] + str(dv1), 11)

    return digs[-2:] == f"{dv1}{dv2}"