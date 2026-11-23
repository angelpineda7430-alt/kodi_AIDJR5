"""Presentación de resultados y generación de informes de texto."""
from analizador import resumir_eventos
from diagnostico import diagnosticar


def construir_informe(eventos, nombre_archivo):
    metricas = resumir_eventos(eventos)
    lineas = [
        "INFORME DE ANÁLISIS DE LOGS",
        f"Archivo: {nombre_archivo}",
        f"Total de eventos: {metricas['total']}",
        f"INFO: {metricas['por_nivel']['INFO']}",
        f"WARNING: {metricas['por_nivel']['WARNING']}",
        f"ERROR: {metricas['por_nivel']['ERROR']}",
        f"Sin clasificar: {metricas['por_nivel']['SIN_CLASIFICAR']}",
        f"Fechas válidas: {metricas['fechas_validas']}",
        f"Líneas malformadas: {metricas['malformadas']}",
        "",
        "DIAGNÓSTICO:",
    ]
    lineas.extend(f"- {item}" for item in diagnosticar(eventos))
    if metricas["eventos_malformados"]:
        lineas.extend(["", "DETALLE DE INCIDENCIAS:"])
        for evento in metricas["eventos_malformados"]:
            lineas.append(f"Línea {evento['numero']}: {', '.join(evento['problemas'])}")
    return "\n".join(lineas)
