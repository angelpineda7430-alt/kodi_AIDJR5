"""Cliente opcional compatible con la API de Chat Completions.

Admite OpenAI y servidores locales compatibles, como Ollama.
Para Ollama no se necesita una clave real: el servidor local no la exige.
"""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ErrorLLM(RuntimeError):
    """Error controlado al comunicarse con el proveedor LLM."""


def disponible():
    proveedor = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if proveedor == "ollama":
        return True
    return bool(os.getenv("OPENAI_API_KEY"))


def consultar(mensajes):
    proveedor = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    api_key = os.getenv("OPENAI_API_KEY")

    if proveedor not in {"openai", "ollama"}:
        raise ErrorLLM("LLM_PROVIDER debe ser 'openai' u 'ollama'.")

    if proveedor == "openai" and not api_key:
        raise ErrorLLM("No se configuró OPENAI_API_KEY.")

    if proveedor == "ollama":
        base_url = os.getenv(
            "OPENAI_BASE_URL", "http://localhost:11434/v1"
        ).rstrip("/")
        modelo = os.getenv("OPENAI_MODEL", "qwen2.5:1.5b")
        # Ollama local no valida esta clave; se envía solo por compatibilidad.
        api_key = "ollama"
    else:
        base_url = os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        ).rstrip("/")
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
        with urlopen(solicitud, timeout=120) as respuesta:
            datos = json.loads(respuesta.read().decode("utf-8"))
        return datos["choices"][0]["message"]["content"]
    except (HTTPError, URLError, TimeoutError, KeyError, IndexError, ValueError) as exc:
        raise ErrorLLM(f"No fue posible consultar el modelo: {exc}") from exc
