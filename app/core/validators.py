from typing import Optional

def normalize_cedula(ced: str) -> str:
    # quita NBSP, espacios internos y extremos
    return "".join(ced.replace("\u00A0", " ").split())

def validar_cedula_ec(cedula: str) -> bool:
    c = normalize_cedula(cedula)
    if len(c) != 10 or not c.isdigit():
        return False
    prov = int(c[:2])
    if prov < 1 or prov > 24:
        return False
    d = list(map(int, c))
    coef = [2,1,2,1,2,1,2,1,2]
    s = 0
    for i in range(9):
        v = d[i] * coef[i]
        s += v - 9 if v >= 10 else v
    dig = (10 - (s % 10)) % 10
    return dig == d[9]
