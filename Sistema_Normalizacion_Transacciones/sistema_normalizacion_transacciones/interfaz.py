import json
from pathlib import Path
from validador import procesar_registros
from metricas import calcular_metricas

RUTA_DEFECTO = Path(__file__).parent / "datos" / "transacciones_prueba.json"

def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    if not isinstance(datos, list):
        raise ValueError("El archivo JSON debe contener una lista de transacciones.")
    return datos

def mostrar_transacciones(transacciones):
    if not transacciones:
        print("\\nNo hay registros para mostrar.")
        return
    print("\\n" + "-" * 105)
    print(f"{'ID':<16} {'MONTO':>13} {'MONEDA':<8} {'FECHA':<27} {'ESTADO':<10} {'FUENTE':<12}")
    print("-" * 105)
    for t in transacciones:
        print(f"{str(t['id']):<16} {str(t['amount']):>13} {str(t['currency']):<8} "
              f"{str(t['timestamp']):<27} {str(t['status']):<10} {str(t['source']):<12}")
    print("-" * 105)

def mostrar_metricas(metricas):
    print("\\n========== MÉTRICAS DEL PROCESAMIENTO ==========")
    print(f"Registros leídos:       {metricas['total_entrada']}")
    print(f"Total procesados:       {metricas['total_procesadas']}")
    print(f"Transacciones válidas:  {metricas['validas']}")
    print(f"Transacciones inválidas:{metricas['invalidas']}")
    print("\\nConteo por estado:")
    for estado in ("SUCCESS", "FAILED", "PENDING"):
        print(f"  {estado:<10}: {metricas['por_estado'].get(estado, 0)}")
    print("\\nTotales por moneda (solo transacciones válidas):")
    for moneda, total in metricas["totales_por_moneda"].items():
        print(f"  {moneda}: {total}")
    print("=" * 50)

def mostrar_invalidas(invalidas):
    if not invalidas:
        print("\\nNo se encontraron transacciones inválidas.")
        return
    for item in invalidas:
        print(f"\\nRegistro #{item['numero_registro']} | ID: {item['transaccion']['id']}")
        for error in item["errores"]:
            print(f"  - {error}")

def ejecutar_interfaz():
    ruta = RUTA_DEFECTO
    try:
        registros = cargar_json(ruta)
        validas, invalidas = procesar_registros(registros)
    except Exception as exc:
        print(f"No fue posible cargar el archivo: {exc}")
        return

    while True:
        print("\\n" + "=" * 58)
        print(" SISTEMA DE NORMALIZACIÓN DE TRANSACCIONES")
        print("=" * 58)
        print(f"Archivo: {ruta.name} | Registros: {len(registros)}")
        print("1. Listar todas las transacciones válidas")
        print("2. Filtrar por estado")
        print("3. Filtrar por moneda")
        print("4. Consultar métricas")
        print("5. Ver transacciones inválidas y sus motivos")
        print("6. Cargar otro archivo JSON")
        print("7. Salir")
        opcion = input("\\nSeleccione una opción: ").strip()

        if opcion == "1":
            mostrar_transacciones(validas)
        elif opcion == "2":
            estado = input("Estado (SUCCESS, FAILED, PENDING): ").strip().upper()
            mostrar_transacciones([t for t in validas if t["status"] == estado])
        elif opcion == "3":
            moneda = input("Moneda (USD, EUR, GBP): ").strip().upper()
            mostrar_transacciones([t for t in validas if t["currency"] == moneda])
        elif opcion == "4":
            mostrar_metricas(calcular_metricas(validas, invalidas, len(registros)))
        elif opcion == "5":
            mostrar_invalidas(invalidas)
        elif opcion == "6":
            nueva_ruta = input("Ruta completa del archivo JSON: ").strip().strip('"')
            try:
                ruta = Path(nueva_ruta)
                registros = cargar_json(ruta)
                validas, invalidas = procesar_registros(registros)
                print(f"Archivo cargado correctamente: {len(registros)} registros.")
            except Exception as exc:
                print(f"Error al cargar archivo: {exc}")
                ruta = RUTA_DEFECTO
                registros = cargar_json(ruta)
                validas, invalidas = procesar_registros(registros)
        elif opcion == "7":
            print("Gracias por utilizar el sistema.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
