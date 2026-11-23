"""Lectura y análisis determinista de archivos de logs."""
from collections import Counter
from datetime import datetime
from pathlib import Path
import re

NIVELES = ("INFO", "WARNING", "ERROR")
PATRON_NIVEL = re.compile(r"^\s*\[([A-Za-z]+)\]\s*(.*)$")
PATRON_FECHA = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:\s+(.*))?$")


def analizar_linea(linea, numero):
    """Convierte una línea en un evento estructurado con sus incidencias."""
    original = linea.rstrip("\r\n")
    contenido = original.strip()
    if not contenido:
        return None

    evento = {
        "numero": numero, "texto": original, "nivel": "SIN_CLASIFICAR",
        "fecha": None, "fecha_valida": False, "mensaje": "", "problemas": []
    }
    coincidencia = PATRON_NIVEL.match(contenido)
    if coincidencia:
        nivel = coincidencia.group(1).upper()
        resto = coincidencia.group(2).strip()
        if nivel in NIVELES:
            evento["nivel"] = nivel
        else:
            evento["problemas"].append(f"nivel desconocido: {nivel}")
    else:
        evento["problemas"].append("falta el nivel [INFO/WARNING/ERROR]")
        resto = contenido

    fecha_match = PATRON_FECHA.match(resto)
    if fecha_match:
        fecha_texto = fecha_match.group(1)
        evento["fecha"] = fecha_texto
        evento["mensaje"] = (fecha_match.group(2) or "").strip()
        try:
            datetime.strptime(fecha_texto, "%Y-%m-%d")
            evento["fecha_valida"] = True
        except ValueError:
            evento["problemas"].append("fecha inexistente o inválida")
    else:
        primer_token = resto.split(maxsplit=1)[0] if resto else ""
        if re.match(r"^\d{4}-\d{2}-\d{2}", primer_token):
            evento["fecha"] = primer_token
            evento["problemas"].append("fecha con formato o valor inválido")
            partes = resto.split(maxsplit=1)
            evento["mensaje"] = partes[1].strip() if len(partes) > 1 else ""
        else:
            evento["problemas"].append("fecha ausente o con formato inválido")
            evento["mensaje"] = resto

    if not evento["mensaje"]:
        evento["problemas"].append("mensaje ausente")
    evento["malformada"] = bool(evento["problemas"])
    return evento


def analizar_archivo(ruta):
    """Lee un archivo UTF-8 y devuelve los eventos no vacíos analizados."""
    ruta = Path(ruta)
    eventos = []
    with ruta.open("r", encoding="utf-8-sig") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            evento = analizar_linea(linea, numero)
            if evento is not None:
                eventos.append(evento)
    return eventos


def resumir_eventos(eventos):
    """Calcula métricas sin depender de un modelo de lenguaje."""
    conteo = Counter(evento["nivel"] for evento in eventos)
    return {
        "total": len(eventos),
        "por_nivel": {nivel: conteo[nivel] for nivel in (*NIVELES, "SIN_CLASIFICAR")},
        "fechas_validas": sum(e["fecha_valida"] for e in eventos),
        "malformadas": sum(e["malformada"] for e in eventos),
        "eventos_error": [e for e in eventos if e["nivel"] == "ERROR"],
        "eventos_malformados": [e for e in eventos if e["malformada"]],
    }
