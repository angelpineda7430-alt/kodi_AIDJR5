# Agente inteligente para análisis de logs

## Objetivo
Refactorizar el analizador original para separar el análisis determinista, el diagnóstico, los reportes y la coordinación de un agente personalizable mediante skills.

## Requisitos
- Python 3.9 o superior.
- Biblioteca estándar de Python.
- Ollama local o una clave de API compatible con Chat Completions (opcional).

## Ejecución
Desde esta carpeta:

```bash
python analizador_logs.py prueba_correcta.txt
```

También puede ejecutarse sin argumento y escribir la ruta cuando se solicite:

```bash
python analizador_logs.py
```

El agente acepta solicitudes como:
- Resume el archivo y muestra las estadísticas.
- Diagnostica los errores y advertencias.
- Genera un informe técnico.

Escriba `salir` para terminar.

## Pruebas unitarias

Desde esta carpeta ejecute:

```bash
python -m unittest discover -s tests -v
```

La suite contiene seis pruebas unitarias para lectura y validación de eventos, fechas, niveles y resumen estadístico.

## Configuración opcional del LLM

### Ollama local

Con Ollama instalado y el modelo descargado, abra CMD en esta carpeta y configure:

```cmd
set LLM_PROVIDER=ollama
set OPENAI_BASE_URL=http://localhost:11434/v1
set OPENAI_MODEL=qwen2.5:1.5b
python analizador_logs.py prueba_correcta.txt
```

En PowerShell, utilice:

```powershell
$env:LLM_PROVIDER="ollama"
$env:OPENAI_BASE_URL="http://localhost:11434/v1"
$env:OPENAI_MODEL="qwen2.5:1.5b"
python analizador_logs.py prueba_correcta.txt
```

No es necesario configurar `OPENAI_API_KEY` para Ollama local. El servidor debe estar iniciado y el modelo debe haberse descargado previamente.

### API compatible con OpenAI

Configure `LLM_PROVIDER=openai`, `OPENAI_API_KEY`, `OPENAI_BASE_URL` y `OPENAI_MODEL`. Nunca incluya claves reales en GitHub.

Sin un proveedor LLM configurado, el sistema utiliza selección local de skills. Ese modo no debe presentarse como razonamiento LLM.

## Arquitectura
- `analizador.py`: lectura, parsing, validación de fechas y métricas.
- `agente.py`: selección de skills y coordinación; valida la acción devuelta por el modelo y admite JSON envuelto en Markdown.
- `cliente_llm.py`: comunicación con Ollama local o API compatible con Chat Completions.
- `diagnostico.py`: hallazgos deterministas.
- `reportes.py`: construcción de informes.
- `interfaz.py`: interacción de consola.
- `skills/*/SKILL.md`: instrucciones reutilizables de cada capacidad.
- `analizador_logs.py`: punto de entrada compatible con el comando anterior.

## Seguridad y límites
- La clave de API, si se utiliza, se obtiene del entorno y no se guarda en el repositorio.
- Ollama se ejecuta localmente; los prompts no necesitan enviarse a un proveedor externo.
- Los logs pueden contener información sensible; revise su contenido antes de compartirlo.
- Python produce las métricas y los hallazgos verificables; el modelo selecciona la skill y redacta explicaciones basadas en esos datos.
- Si no hay LLM disponible o su respuesta no puede validarse, se usa el enrutamiento local por palabras clave.
