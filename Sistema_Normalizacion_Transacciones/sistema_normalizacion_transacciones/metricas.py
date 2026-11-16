from collections import Counter, defaultdict
from decimal import Decimal

def calcular_metricas(validas, invalidas, total_entrada):
    por_estado = Counter(t["status"] for t in validas)
    por_moneda = defaultdict(Decimal)
    for transaccion in validas:
        por_moneda[transaccion["currency"]] += Decimal(transaccion["amount"])

    return {
        "total_entrada": total_entrada,
        "total_procesadas": len(validas) + len(invalidas),
        "validas": len(validas),
        "invalidas": len(invalidas),
        "por_estado": dict(por_estado),
        "totales_por_moneda": {k: str(v) for k, v in sorted(por_moneda.items())}
    }
