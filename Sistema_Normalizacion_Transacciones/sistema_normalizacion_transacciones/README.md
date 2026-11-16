# Sistema de normalización de transacciones

## Requisitos
- Python 3.9 o superior.
- No requiere instalar librerías externas: utiliza la biblioteca estándar de Python.

## Ejecución en Windows
1. Extraiga el ZIP en una carpeta.
2. Abra PowerShell o CMD dentro de la carpeta `sistema_normalizacion_transacciones`.
3. Ejecute: `python main.py`
4. Seleccione una opción del menú.

## Archivos
- `main.py`: punto de entrada.
- `normalizador.py`: detecta fuentes y transforma datos al esquema común.
- `validador.py`: valida registros, separa inválidos y detecta duplicados.
- `metricas.py`: calcula conteos y totales por moneda.
- `interfaz.py`: menú interactivo, listados y filtros.
- `reglas.json`: configuración/documentación de reglas.
- `datos/transacciones_prueba.json`: datos de prueba válidos e inconsistentes.
- `NOTA_TECNICA.md`: decisiones de diseño y uso de IA.

## Esquema normalizado
Cada transacción válida contiene:
`id`, `amount`, `currency`, `timestamp`, `status`, `source`.

## Reglas y decisiones de diseño
- Los estados se convierten a `SUCCESS`, `FAILED` o `PENDING`.
- Se admiten USD, EUR y GBP.
- Los montos se convierten a decimal y deben ser mayores que cero.
- Las fechas se convierten a ISO-8601. Las fechas sin zona horaria se interpretan como UTC.
- Los registros con errores no se eliminan silenciosamente: se separan y se muestran con sus motivos.
- Los identificadores duplicados se consideran inválidos.
- Los totales se calculan por moneda; no se suman monedas distintas ni se realiza conversión cambiaria.

## Pruebas
El archivo de prueba contiene registros de las tres estructuras del enunciado, además de casos con monto cero, moneda no soportada, fecha incorrecta, estado desconocido, identificador duplicado y estado ausente.
