# Nota técnica – Sistema de normalización de transacciones

## Decisiones de diseño
Se definió un esquema común con seis atributos: identificador (`id`), monto (`amount`), moneda (`currency`), fecha y hora (`timestamp`), estado (`status`) y fuente (`source`). Se separaron las responsabilidades en módulos para facilitar el mantenimiento y las pruebas.

El sistema identifica tres estructuras de entrada: Fuente A (`id`, `amount`, `currency`, `timestamp`, `status`), Fuente B (`transaction_id`, `total`, `currency_code`, `created_at`, `state`) y Fuente C (`ref`, `amount`, `date`, `result`).

Los montos se convierten a decimal. Se admiten USD, EUR y GBP; se reconoce el símbolo de dólar, euro o libra cuando no viene un código explícito. Los estados se mapean a SUCCESS, FAILED y PENDING. Las fechas reconocidas se convierten a ISO-8601; cuando la fecha no contiene zona horaria se interpreta como UTC.

Se considera inválido un registro sin identificador, monto, moneda, fecha o estado; también si el monto no es numérico o no es mayor que cero, la moneda no está soportada, la fecha no se reconoce, el estado no está mapeado o el identificador está duplicado. Los registros inválidos se separan y se conserva el motivo de cada error.

Las métricas incluyen total leído/procesado, cantidad válida e inválida, conteo por estado y sumatoria por moneda. No se mezclan importes de monedas diferentes ni se realiza conversión cambiaria, porque no se proporcionó una tasa de cambio.

## Uso de IA
La IA se utilizó como apoyo para proponer la separación modular, ejemplos de parsing, validaciones y opciones de interfaz. Las reglas de negocio, el esquema normalizado y los criterios de aceptación deben ser revisados y aprobados por el estudiante según los requisitos de la actividad. Se recomienda explicar y justificar estas decisiones durante la presentación.

## Ajustes y limitaciones
Se incorporaron datos de prueba con inconsistencias para comprobar el manejo de errores. La interfaz elegida es CLI interactiva, permitiendo listar, filtrar, consultar métricas, revisar inválidos y cargar otro archivo JSON. Las monedas y formatos admitidos están documentados en `reglas.json`.
