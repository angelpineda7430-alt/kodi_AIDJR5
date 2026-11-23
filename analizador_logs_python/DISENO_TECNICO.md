# Diseño técnico y decisiones de refactorización

## 1. Situación inicial
La versión original concentraba en un único archivo la lectura del archivo, el análisis de líneas, la clasificación de eventos, el cálculo de métricas y la presentación del resumen. Las reglas eran deterministas y no existía un agente LLM ni skills independientes.

## 2. Objetivo de la refactorización
Separar responsabilidades y añadir un agente que pueda seleccionar capacidades especializadas documentadas como skills. El analizador determinista se conserva como fuente de verdad para los datos y las métricas.

## 3. Arquitectura resultante
- **analizador.py:** lectura, parsing, validación de fechas y métricas.
- **agente.py:** coordinación y selección de skills; limpia respuestas JSON envueltas en Markdown y valida que la acción pertenezca al catálogo permitido.
- **cliente_llm.py:** comunicación opcional con Ollama local o una API compatible con Chat Completions.
- **diagnostico.py:** hallazgos verificables a partir de los eventos.
- **reportes.py:** construcción de informes.
- **interfaz.py:** interacción de consola.
- **skills/**: instrucciones específicas para análisis, diagnóstico y reportes.

## 4. Diseño de skills
Cada skill cuenta con un archivo SKILL.md que define su nombre, descripción, cuándo debe utilizarse y sus instrucciones. Las skills encapsulan capacidades específicas y pueden ser reutilizadas por el agente.

## 5. Personalización del agente
El agente recibe una solicitud en lenguaje natural. Cuando el proveedor LLM está configurado, solicita al modelo que seleccione una de las skills permitidas mediante una respuesta JSON. La selección se valida contra el catálogo local antes de ejecutar una capacidad.

Algunos modelos entregan el JSON dentro de un bloque Markdown. El agente elimina esos delimitadores antes de interpretar la respuesta. Si el LLM no está configurado o la respuesta no es válida, se utiliza un enrutamiento local explícito. La interfaz informa qué modo de selección se utilizó; el modo local no se presenta como razonamiento LLM.

## 6. Separación entre IA y lógica determinista
Python realiza el conteo de eventos, la validación de fechas y la identificación de incidencias. Para el diagnóstico, Python proporciona al modelo el resumen y la evidencia por línea: número, nivel, problemas detectados y texto original. El LLM redacta una explicación basada en esos resultados; no debe inventar métricas ni causas raíz que no estén demostradas. Esta separación facilita verificar las cifras y reduce errores de interpretación.

## 7. Proveedor LLM local y seguridad
Ollama permite ejecutar un modelo local mediante su endpoint compatible con Chat Completions, sin requerir una clave API real. También se admite un proveedor API compatible con OpenAI, cuya clave se obtiene de variables de entorno y no se incluye en el repositorio. Los archivos de logs pueden contener información sensible; deben revisarse y anonimizarse antes de enviarlos a un servicio externo.

## 8. Pruebas y validación
La suite de pruebas unitarias se ejecutó con `python -m unittest discover -s tests -v`: seis pruebas finalizaron correctamente. También se comprobó manualmente que Ollama expone el modelo `qwen2.5:1.5b`, que el endpoint Chat Completions responde y que el agente selecciona la skill de diagnóstico en modo LLM y presenta hallazgos con números de línea. Conviene repetir las pruebas con los archivos de ejemplo correcto e inconsistente antes de cada entrega.

## 9. Uso de IA como apoyo
La IA se utiliza como apoyo para proponer la separación modular, el diseño de skills y la coordinación del agente. Las decisiones de arquitectura, las reglas de validación y los resultados se revisan mediante pruebas. La aprobación final del diseño y la explicación del funcionamiento corresponden al estudiante.
