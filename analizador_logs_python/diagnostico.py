"""Diagnóstico basado en reglas explícitas y resultados verificables."""

def diagnosticar(eventos):
    """Agrupa hallazgos; no afirma causas que no estén en el contenido."""
    resumen = []
    errores = [e for e in eventos if e["nivel"] == "ERROR"]
    advertencias = [e for e in eventos if e["nivel"] == "WARNING"]
    malformados = [e for e in eventos if e["malformada"]]

    if errores:
        resumen.append(f"Se encontraron {len(errores)} eventos ERROR que requieren revisión.")
    if advertencias:
        resumen.append(f"Se encontraron {len(advertencias)} eventos WARNING.")
    if malformados:
        resumen.append(f"Hay {len(malformados)} líneas malformadas o incompletas.")
    if not resumen:
        resumen.append("No se detectaron errores, advertencias ni líneas malformadas.")
    return resumen
