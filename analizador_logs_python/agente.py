"""Agente que selecciona skills y coordina herramientas locales verificables."""
import json
from pathlib import Path

from cliente_llm import disponible, consultar, ErrorLLM
from analizador import resumir_eventos
from diagnostico import diagnosticar
from reportes import construir_informe

RUTA_SKILLS = Path(__file__).parent / "skills"


def cargar_skills():
    """Carga las instrucciones documentadas de las skills instaladas."""
    instrucciones = {}
    for archivo in sorted(RUTA_SKILLS.glob("*/SKILL.md")):
        instrucciones[archivo.parent.name] = archivo.read_text(encoding="utf-8")
    return instrucciones


def seleccionar_accion(pregunta, skills):
    """Solicita al LLM una acción permitida; usa reglas locales si no hay API."""
    if disponible():
        catalogo = ", ".join(skills)
        mensajes = [
            {"role": "system", "content":
             "Eres un agente de análisis de logs. Selecciona una sola skill. "
             "Responde exclusivamente JSON con la clave accion. "
             f"Acciones permitidas: {catalogo}. No inventes acciones."},
            {"role": "user", "content": pregunta}
        ]
        try:
            respuesta = consultar(mensajes)
            datos = json.loads(respuesta)
            accion = datos.get("accion")
            if accion in skills:
                return accion, "LLM"
        except (ErrorLLM, json.JSONDecodeError, AttributeError):
            pass

    texto = pregunta.lower()
    if any(p in texto for p in ("informe", "reporte", "documento")):
        return "reportes", "reglas locales"
    if any(p in texto for p in ("causa", "diagnóstico", "diagnostico", "gravedad", "recomend")):
        return "diagnostico", "reglas locales"
    if any(p in texto for p in ("estadística", "estadistica", "métrica", "metrica", "resumen", "cuántos", "cuantos")):
        return "analisis", "reglas locales"
    return "analisis", "reglas locales"


def ejecutar(pregunta, eventos, nombre_archivo):
    """Ejecuta la skill elegida y devuelve una respuesta sustentada en datos."""
    skills = cargar_skills()
    accion, modo = seleccionar_accion(pregunta, skills)
    if accion == "diagnostico":
        resultado = "\n".join(f"- {x}" for x in diagnosticar(eventos))
    elif accion == "reportes":
        resultado = construir_informe(eventos, nombre_archivo)
    else:
        m = resumir_eventos(eventos)
        resultado = (
            f"Archivo: {nombre_archivo}\n"
            f"Eventos: {m['total']}\n"
            f"INFO: {m['por_nivel']['INFO']} | "
            f"WARNING: {m['por_nivel']['WARNING']} | "
            f"ERROR: {m['por_nivel']['ERROR']} | "
            f"Sin clasificar: {m['por_nivel']['SIN_CLASIFICAR']}\n"
            f"Fechas válidas: {m['fechas_validas']}\n"
            f"Líneas malformadas: {m['malformadas']}"
        )

    if modo == "LLM" and disponible():
        try:
            resultado = consultar([
                {"role": "system", "content":
                 "Explica en español los resultados técnicos proporcionados. "
                 "No agregues cifras ni causas que no estén en los datos. "
                 "Distingue hechos de hipótesis."},
                {"role": "user", "content": resultado}
            ])
        except ErrorLLM:
            pass
    return accion, modo, resultado
