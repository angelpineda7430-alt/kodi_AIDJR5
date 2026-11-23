# Agente inteligente para análisis de logs

## Objetivo
Refactorizar el analizador original para separar el análisis determinista, el diagnóstico, los reportes y la coordinación de un agente personalizable mediante skills.

## Requisitos
- Python 3.9 o superior.
- Biblioteca estándar de Python.
- Una clave de API compatible con Chat Completions es opcional para habilitar selección y explicación mediante LLM.

## Ejecución
Desde esta carpeta:

\`\`\`bash
python analizador_logs.py prueba_correcta.txt
\`\`\`

También puede ejecutarse sin argumento y escribir la ruta cuando se solicite:

\`\`\`bash
python analizador_logs.py
\`\`\`

El agente acepta solicitudes como:
- Resume el archivo y muestra las estadísticas.
- Diagnostica los errores y advertencias.
- Genera un informe técnico.

Escriba \`salir\` para terminar.

## Configuración opcional del LLM
Configure las variables de entorno \`OPENAI_API_KEY\`, \`OPENAI_BASE_URL\` y \`OPENAI_MODEL\`. El valor predeterminado del modelo es \`gpt-4o-mini\`. Nunca incluya claves reales en GitHub.

En Windows PowerShell:

\`\`\`powershell
$env:OPENAI_API_KEY="SU_CLAVE"
$env:OPENAI_MODEL="gpt-4o-mini"
python analizador_logs.py prueba_correcta.txt
\`\`\`

Sin clave configurada, el sistema utiliza selección local de skills. Ese modo no debe presentarse como razonamiento LLM.

## Arquitectura
- \`analizador.py\`: lectura, parsing, validación de fechas y métricas.
- \`agente.py\`: selección de skills y coordinación.
- \`cliente_llm.py\`: comunicación opcional con API compatible con Chat Completions.
- \`diagnostico.py\`: hallazgos deterministas.
- \`reportes.py\`: construcción de informes.
- \`interfaz.py\`: interacción de consola.
- \`skills/*/SKILL.md\`: instrucciones reutilizables de cada capacidad.
- \`analizador_logs.py\`: punto de entrada compatible con el comando anterior.

## Seguridad y límites
- La clave LLM se obtiene del entorno y no se guarda en archivos del proyecto.
- Los logs pueden contener información sensible. Revise y anonimice su contenido antes de enviarlo a un proveedor externo.
- Python produce las métricas; el modelo selecciona la skill y redacta explicaciones.
- Si no hay LLM disponible, se usa el enrutamiento local por palabras clave.
