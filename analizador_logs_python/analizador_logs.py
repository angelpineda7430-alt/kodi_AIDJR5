#!/usr/bin/env python3
"""
Analizador de logs
Formato esperado: [NIVEL] AAAA-MM-DD mensaje
Niveles admitidos: INFO, WARNING, ERROR.

Decisiones de validacion:
- Cada linea no vacia representa un evento y se incluye en el total.
- Las lineas vacias se ignoran (no son eventos).
- Se reconoce el nivel aunque falte la fecha o el mensaje.
- Una fecha solo es valida si existe y cumple AAAA-MM-DD como fecha real.
- Una linea es malformada/incompleta si falta el nivel reconocido, la fecha
  valida o el mensaje. Los niveles desconocidos se cuentan como SIN_CLASIFICAR.
"""

from collections import Counter
from datetime import datetime
from pathlib import Path
import re
import sys

NIVELES = ("INFO", "WARNING", "ERROR")
PATRON_NIVEL = re.compile(r"^\s*\[([A-Za-z]+)\]\s*(.*)$")
PATRON_FECHA = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:\s+(.*))?$")


def seleccionar_archivo():
    """Permite elegir un archivo mediante ventana; si no es posible, pide ruta."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        raiz = tk.Tk()
        raiz.withdraw()
        ruta = filedialog.askopenfilename(
            title="Seleccione el archivo de logs",
            filetypes=[("Archivos de texto", "*.txt *.log"), ("Todos los archivos", "*.*")]
        )
        raiz.destroy()
        if ruta:
            return Path(ruta)
    except Exception:
        # En entornos sin interfaz grafica se usa la entrada por consola.
        pass

    ruta = input("Ingrese la ruta del archivo de logs: ").strip().strip('"')
    return Path(ruta) if ruta else None


def analizar_linea(linea, numero):
    """Analiza una linea y devuelve sus campos y observaciones."""
    original = linea.rstrip("\r\n")
    contenido = original.strip()
    resultado = {
        "numero": numero,
        "texto": original,
        "nivel": "SIN_CLASIFICAR",
        "fecha": None,
        "fecha_valida": False,
        "mensaje": "",
        "problemas": []
    }

    if not contenido:
        return None  # Las lineas vacias no se consideran eventos.

    coincidencia = PATRON_NIVEL.match(contenido)
    if not coincidencia:
        resultado["problemas"].append("falta el nivel [INFO/WARNING/ERROR]")
        resto = contenido
    else:
        nivel_leido = coincidencia.group(1).upper()
        resto = coincidencia.group(2).strip()
        if nivel_leido in NIVELES:
            resultado["nivel"] = nivel_leido
        else:
            resultado["problemas"].append(f"nivel desconocido: {nivel_leido}")

    fecha_match = PATRON_FECHA.match(resto)
    if fecha_match:
        fecha_texto = fecha_match.group(1)
        resultado["fecha"] = fecha_texto
        resultado["mensaje"] = (fecha_match.group(2) or "").strip()
        try:
            # strptime verifica tanto la forma como la existencia de la fecha.
            datetime.strptime(fecha_texto, "%Y-%m-%d")
            resultado["fecha_valida"] = True
        except ValueError:
            resultado["problemas"].append("fecha inexistente o invalida")
    else:
        # Si comienza con una cadena con apariencia de fecha, se informa
        # especificamente que su formato/valor es incorrecto.
        primer_token = resto.split(maxsplit=1)[0] if resto else ""
        if re.match(r"^\d{4}-\d{2}-\d{2}", primer_token):
            resultado["fecha"] = primer_token
            resultado["problemas"].append("fecha con formato o valor invalido")
            partes = resto.split(maxsplit=1)
            resultado["mensaje"] = partes[1].strip() if len(partes) > 1 else ""
        else:
            resultado["problemas"].append("fecha ausente o con formato invalido")
            resultado["mensaje"] = resto

    if not resultado["mensaje"]:
        resultado["problemas"].append("mensaje ausente")

    resultado["malformada"] = bool(resultado["problemas"])
    return resultado


def analizar_archivo(ruta):
    """Lee el archivo UTF-8 y analiza sus lineas no vacias."""
    eventos = []
    with ruta.open("r", encoding="utf-8-sig") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            evento = analizar_linea(linea, numero)
            if evento is not None:
                eventos.append(evento)
    return eventos


def mostrar_resumen(eventos, ruta):
    conteo = Counter(evento["nivel"] for evento in eventos)
    malformadas = [e for e in eventos if e["malformada"]]
    validas = sum(1 for e in eventos if e["fecha_valida"])

    print("\n" + "=" * 62)
    print("             RESUMEN DEL ANALISIS DE LOGS")
    print("=" * 62)
    print(f"Archivo:                  {ruta}")
    print(f"Total de eventos:         {len(eventos)}")
    print(f"Eventos INFO:             {conteo['INFO']}")
    print(f"Eventos WARNING:          {conteo['WARNING']}")
    print(f"Eventos ERROR:             {conteo['ERROR']}")
    print(f"Sin clasificar:            {conteo['SIN_CLASIFICAR']}")
    print(f"Fechas validas:            {validas}")
    print(f"Lineas malformadas:        {len(malformadas)}")
    print("-" * 62)

    if malformadas:
        print("DETALLE DE LINEAS CON PROBLEMAS")
        for evento in malformadas:
            print(f"Linea {evento['numero']}: {', '.join(evento['problemas'])}")
            print(f"  > {evento['texto']}")
    else:
        print("No se encontraron lineas malformadas.")
    print("=" * 62)


def main():
    if len(sys.argv) > 1:
        ruta = Path(sys.argv[1].strip('"'))
    else:
        ruta = seleccionar_archivo()

    if ruta is None:
        print("No se selecciono ningun archivo. Operacion cancelada.")
        return 1
    if not ruta.exists() or not ruta.is_file():
        print(f"Error: no existe un archivo valido en: {ruta}")
        return 1

    try:
        eventos = analizar_archivo(ruta)
    except UnicodeDecodeError:
        print("Error: el archivo no esta codificado en UTF-8.")
        return 1
    except OSError as error:
        print(f"No fue posible leer el archivo: {error}")
        return 1

    mostrar_resumen(eventos, ruta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
