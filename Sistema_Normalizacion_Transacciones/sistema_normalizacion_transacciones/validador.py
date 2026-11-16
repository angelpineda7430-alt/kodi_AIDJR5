from normalizador import normalizar

def procesar_registros(registros):
    validas = []
    invalidas = []
    ids_vistos = set()

    for numero, registro in enumerate(registros, start=1):
        try:
            normalizada, errores = normalizar(registro)
        except Exception as exc:
            normalizada = {"id": None, "amount": None, "currency": None,
                           "timestamp": None, "status": None, "source": "DESCONOCIDA"}
            errores = [f"Registro no procesable: {exc}"]

        identificador = normalizada.get("id")
        if identificador and identificador in ids_vistos:
            errores.append(f"Identificador duplicado: {identificador}")
        elif identificador:
            ids_vistos.add(identificador)

        elemento = {"numero_registro": numero, "transaccion": normalizada, "errores": errores}
        if errores:
            invalidas.append(elemento)
        else:
            validas.append(normalizada)

    return validas, invalidas
