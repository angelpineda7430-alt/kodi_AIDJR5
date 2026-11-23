# Diseño técnico y decisiones de refactorización

## 1. Situación inicial
La versión original concentraba en un único archivo la lectura del archivo, el análisis de líneas, la clasificación de eventos, el cálculo de métricas y la presentación del resumen. Las reglas eran deterministas y no existía un agente LLM ni skills independientes.

## 2. Objetivo de la refactorización
Separar responsabilidades y añadir un agente que pueda seleccionar capacidades especializadas documentadas como skills. El analizador determinista se conserva como fuente de verdad para los datos y las métricas.

## 3. Arquitectura resultante
- **analizador.py:** lectura, parsing, validación de fechas y métricas.
- **agente.py:** coordinación y selección de skills.
- **cliente_llm.py:** comunicación opcional con una API compatible con Chat Completions.
- **diagnostico.py:** hallazgos verificables a partir de los eventos.
- **reportes.py:** construcción de informes.
- **interfaz.py:** interacción de consola.
- **skills/**: instrucciones específicas para análisis, diagnóstico y reportes.

## 4. Diseño de skills
Cada skill cuenta con un archivo SKILL.md que define su nombre, descripción, cuándo debe utilizarse y sus instrucciones. Las skills encapsulan capacidades específicas y pueden ser reutilizadas por el agente.

## 5. Personalización del agente
El agente recibe una solicitud en lenguaje natural. Cuando el proveedor LLM está configurado, solicita al modelo que seleccione una de las skills permitidas mediante una respuesta JSON. La selección se valida contra el catálogo local antes de ejecutar una capacidad.

Si el LLM no está configurado o la respuesta no es válida, se utiliza un enrutamiento local explícito. La interfaz informa qué modo de selección se utilizó; el modo local no se presenta como razonamiento LLM.

## 6. Separación entre IA y lógica determinista
Python realiza el conteo de eventos, la validación de fechas y la identificación de incidencias. El LLM no inventa ni calcula métricas: selecciona la capacidad y puede redactar una explicación basada en resultados producidos por el programa. Esto facilita verificar las cifras y reduce errores de interpretación.

## 7. Seguridad
La clave de API se obtiene de variables de entorno y no se incluye en el repositorio. Los archivos de logs pueden contener información sensible; deben anonimizarse antes de enviarlos a un servicio externo.

## 8. Pruebas y validación
Se deben ejecutar los archivos de prueba originales, tanto el correcto como el inconsistente, y comprobar que el total de eventos, los niveles, las fechas válidas y las líneas malformadas coinciden con el contenido del archivo. También debe probarse el modo sin clave LLM y, si se dispone de credenciales, el modo conectado.

## 9. Uso de IA como apoyo
La IA se utiliza como apoyo para proponer la separación modular, el diseño de skills y la coordinación del agente. Las decisiones de arquitectura, las reglas de validación y los resultados se deben revisar mediante pruebas. La aprobación final del diseño y la explicación del funcionamiento corresponden al estudiante.
