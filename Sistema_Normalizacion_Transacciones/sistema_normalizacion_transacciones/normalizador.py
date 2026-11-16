import re
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone

# Esquema común:
# id, amount (Decimal), currency (ISO 4217), timestamp (ISO 8601),
# status (SUCCESS/FAILED/PENDING), source (nombre de la fuente).

ESTADOS = {
    "completed": "SUCCESS", "complete": "SUCCESS", "ok": "SUCCESS",
    "success": "SUCCESS", "successful": "SUCCESS", "approved": "SUCCESS",
    "failed": "FAILED", "failure": "FAILED", "error": "FAILED",
    "rejected": "FAILED", "declined": "FAILED",
    "pending": "PENDING", "processing": "PENDING", "in_progress": "PENDING"
}

SIMBOLOS_MONEDA = {"$": "USD", "€": "EUR", "£": "GBP"}

def detectar_fuente(registro):
    if "transaction_id" in registro or "total" in registro:
        return "FUENTE_B"
    if "ref" in registro or "result" in registro:
        return "FUENTE_C"
    if "id" in registro or "amount" in registro:
        return "FUENTE_A"
    return "DESCONOCIDA"

def obtener_monto(valor):
    if valor is None:
        raise ValueError("Monto ausente")
    if isinstance(valor, (int, float, Decimal)):
        monto = Decimal(str(valor))
    else:
        texto = str(valor).strip().replace(" ", "")
        # Admite formatos como 1,234.56 y 1.234,56.
        texto = re.sub(r"[^0-9,.\-]", "", texto)
        if not texto or texto in {"-", ".", ","}:
            raise ValueError("Formato de monto no reconocido")
        if "," in texto and "." in texto:
            if texto.rfind(",") > texto.rfind("."):
                texto = texto.replace(".", "").replace(",", ".")
            else:
                texto = texto.replace(",", "")
        elif "," in texto:
            partes = texto.split(",")
            texto = "".join(partes[:-1]) + "." + partes[-1] if len(partes[-1]) in (1, 2) else "".join(partes)
        monto = Decimal(texto)
    if not monto.is_finite():
        raise ValueError("Monto no numérico")
    return monto

def obtener_moneda(registro, monto_original):
    codigo = registro.get("currency") or registro.get("currency_code")
    if codigo:
        return str(codigo).strip().upper()
    texto = str(monto_original)
    for simbolo, codigo in SIMBOLOS_MONEDA.items():
        if simbolo in texto:
            return codigo
    return None

def obtener_fecha(valor):
    if not valor:
        raise ValueError("Fecha ausente")
    texto = str(valor).strip()
    # Se admiten ISO-8601 y formatos habituales de las fuentes de ejemplo.
    formatos = (
        "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d"
    )
    try:
        fecha = datetime.fromisoformat(texto.replace("Z", "+00:00"))
    except ValueError:
        fecha = None
        for formato in formatos:
            try:
                fecha = datetime.strptime(texto, formato)
                break
            except ValueError:
                pass
    if fecha is None:
        raise ValueError(f"Formato de fecha no reconocido: {texto}")
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=timezone.utc)
    return fecha.isoformat(timespec="seconds")

def normalizar(registro):
    if not isinstance(registro, dict):
        raise ValueError("Cada transacción debe ser un objeto JSON")

    fuente = detectar_fuente(registro)
    identificador = registro.get("id") or registro.get("transaction_id") or registro.get("ref")
    monto_original = registro.get("amount")
    if monto_original is None:
        monto_original = registro.get("total")

    moneda = obtener_moneda(registro, monto_original)
    fecha_original = registro.get("timestamp") or registro.get("created_at") or registro.get("date")
    estado_original = registro.get("status") or registro.get("state") or registro.get("result")

    errores = []
    if identificador is None or not str(identificador).strip():
        errores.append("Identificador ausente")
    try:
        monto = obtener_monto(monto_original)
        if monto <= 0:
            errores.append("El monto debe ser mayor que cero")
    except (ValueError, InvalidOperation) as exc:
        monto = None
        errores.append(str(exc))

    if not moneda:
        errores.append("Moneda ausente y no detectable")
    else:
        moneda = moneda.upper()
        if moneda not in {"USD", "EUR", "GBP"}:
            errores.append(f"Moneda no soportada: {moneda}")

    try:
        fecha = obtener_fecha(fecha_original)
    except ValueError as exc:
        fecha = None
        errores.append(str(exc))

    estado_clave = str(estado_original).strip().lower() if estado_original is not None else ""
    estado = ESTADOS.get(estado_clave)
    if estado is None:
        errores.append(f"Estado ausente o no reconocido: {estado_original}")

    normalizada = {
        "id": str(identificador).strip() if identificador is not None else None,
        "amount": str(monto) if monto is not None else None,
        "currency": moneda,
        "timestamp": fecha,
        "status": estado,
        "source": fuente
    }
    return normalizada, errores
