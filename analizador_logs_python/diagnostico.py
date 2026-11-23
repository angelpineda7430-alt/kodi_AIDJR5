"""Diagnóstico basado en reglas explícitas y resultados verificables."""

def diagnosticar(eventos):
    """Agrupa hallazgos; no afirma causas que no estén en el contenido."""
    resumen = []
    errores = [e for e in eventos if e["nivel"] == "ERROR"]
    advertencias = [e for e in eventos if e["nivel"] == "WARNING"]
    malformados = [e for e in eventos if e["malformada"]]

    if errores:
        cantidad = len(errores)
        sustantivo = "evento" if cantidad == 1 else "eventos"
        resumen.append(f"Se encontraron {cantidad} {sustantivo} ERROR que requieren revisión.")
    if advertencias:
        cantidad = len(advertencias)
        sustantivo = "advertencia" if cantidad == 1 else "advertencias"
        resumen.append(f"Se encontraron {cantidad} {sustantivo} WARNING.")
    if malformados:
        resumen.append(f"Hay {len(malformados)} líneas malformadas o incompletas.")
    if not resumen:
        resumen.append("No se detectaron errores, advertencias ni líneas malformadas.")
    return resumen
