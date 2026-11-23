"""Cliente opcional compatible con la API de Chat Completions.

La clave se lee desde OPENAI_API_KEY. Nunca se almacena en el repositorio.
El análisis de logs sigue funcionando sin conexión a un proveedor LLM.
"""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ErrorLLM(RuntimeError):
    """Error controlado al comunicarse con el proveedor LLM."""


def disponible():
    return bool(os.getenv("OPENAI_API_KEY"))


def consultar(mensajes):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ErrorLLM("No se configuró OPENAI_API_KEY.")

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    modelo = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    payload = json.dumps({
        "model": modelo, "messages": mensajes, "temperature": 0.2
    }).encode("utf-8")
    solicitud = Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urlopen(solicitud, timeout=45) as respuesta:
            datos = json.loads(respuesta.read().decode("utf-8"))
        return datos["choices"][0]["message"]["content"]
    except (HTTPError, URLError, TimeoutError, KeyError, IndexError, ValueError) as exc:
        raise ErrorLLM(f"No fue posible consultar el modelo: {exc}") from exc
