"""Interfaz de consola para el agente de análisis de logs."""
from pathlib import Path
import argparse

from analizador import analizar_archivo
from agente import ejecutar
from cliente_llm import disponible


def main():
    parser = argparse.ArgumentParser(description="Agente inteligente para análisis de logs")
    parser.add_argument("archivo", nargs="?", help="Ruta del archivo TXT o LOG")
    args = parser.parse_args()

    ruta = Path(args.archivo) if args.archivo else None
    if ruta is None:
        ruta_texto = input("Ruta del archivo de logs: ").strip().strip('"')
        ruta = Path(ruta_texto) if ruta_texto else None
    if ruta is None or not ruta.is_file():
        print("Error: seleccione una ruta válida.")
        return 1

    try:
        eventos = analizar_archivo(ruta)
    except (OSError, UnicodeError) as exc:
        print(f"No fue posible leer el archivo: {exc}")
        return 1

    print(f"Archivo cargado: {ruta.name} ({len(eventos)} eventos)")
    print("Modo LLM: disponible" if disponible() else
          "Modo LLM: no configurado; se utilizará selección local de skills.")
    print("Escriba una solicitud o 'salir' para terminar.")

    while True:
        pregunta = input("\n¿Qué desea hacer? ").strip()
        if pregunta.lower() in {"salir", "exit", "q"}:
            print("Análisis finalizado.")
            break
        if not pregunta:
            continue
        accion, modo, resultado = ejecutar(pregunta, eventos, ruta.name)
        print(f"\n[Skill: {accion} | Selección: {modo}]")
        print(resultado)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
