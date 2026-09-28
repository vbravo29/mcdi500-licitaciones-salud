# Aporte F3: algoritmos y eficiencia

**Responsable:** Víctor Bravo Barrera · **Grupo:** 5 · **Fecha:** 26 de septiembre de 2026

Este texto es la sección técnica preparada para integrar al informe grupal. No sustituye el informe institucional ni los aportes de lectura y validación de los demás integrantes.

## Problema y continuidad con F2

Se calcula la proporción de ofertas ganadoras por tamaño de proveedor y tipo de licitación, restringiendo a procesos adjudicados. Se mantiene la unidad oferta por ítem: una licitación puede aparecer varias veces. No se deduplica por licitación ni se infiere causalidad.

El denominador de cada grupo suma ganadoras y perdedoras. Los resultados desconocidos o faltantes se informan por separado, y un denominador cero produce un porcentaje no definido. Los totales se obtienen sumando conteos, nunca promediando porcentajes parciales.

## Implementaciones y arquitectura

`src/analisis.py` conserva `tabla_proporciones` como referencia F2 y añade las variantes iterativa, recursiva y agrupada. Las tres comparten preparación y construcción de salida. No se modificaron los módulos de lectura, entorno, limpieza, validación ni ejecución existentes.

La versión iterativa mantiene tres contadores por grupo en un diccionario. La recursiva divide intervalos de índices y combina diccionarios parciales; deja de dividir con bloques de hasta 256 registros. Ese umbral es una elección explícita, no un óptimo demostrado. La versión agrupada utiliza una agrupación por grupo y código de resultado mediante pandas (The pandas development team, s. f.).

La recursividad aplica una descomposición útil del conteo en resúmenes combinables, pero aquí es secuencial. No se crean copias de mitades en cada llamada. Para la muestra de 100 filas, el bloque base de 256 evita divisiones: diferencias pequeñas frente a la iterativa no deben atribuirse a una mejora recursiva.

## Verificación

Ocho pruebas algorítmicas y seis pruebas POO existentes superadas. Se utilizaron un resultado manual conocido, comparación contra F2, grupos sin resultados válidos, NA, categorías inválidas, vacíos, otros estados, columnas ausentes, índices repetidos y muestras aleatorias con semilla. Las variantes coinciden también en las dos agrupaciones del dataset real y preservan la entrada. Las pruebas recursivas incluyen bloques de 1, 3 y 256 filas.

La función F2 se conserva sin cambios: ante ausencia de `ResultadoOferta` lanza `AttributeError` por su acceso mediante atributo; las nuevas variantes utilizan acceso por columna y lanzan `KeyError`. Las pruebas documentan esa diferencia de excepción para entradas inválidas.

## Método de medición

Se usó `timeit` con siete rondas de tres ejecuciones y orden alternado con semilla 2026, calentamiento y validación previos. Se presentan mínimo, mediana y cuartiles; el mínimo ayuda a interpretar interferencias de otros procesos y los cuartiles describen esta sesión, sin constituir intervalos de confianza (Python Software Foundation, s. f.-a).

Se midieron cuatro tamaños: 100, 1.000, 10.000 y 44.226 filas, en muestras anidadas de una permutación reproducible. Cada comparación recibe el mismo DataFrame. El tiempo incluye filtro, conversión de resultados, conteo y formato de salida. Excluye carga del CSV, limpieza, selección de muestras y comprobación de equivalencia. Los datos se leen con las siete columnas del análisis y tipos definidos, según la comparación de lectura aportada por Mauricio (sección 12 del notebook).

Los picos de memoria se obtuvieron en tres ejecuciones separadas con `tracemalloc`, sin instrumentar los tiempos. Se excluye la entrada ya cargada. La métrica describe asignaciones rastreadas y no equivale a memoria total del proceso ni garantiza cubrir toda la memoria nativa (Python Software Foundation, s. f.-b).

El arnés separa preparación del caso, temporización, memoria y resumen. Reutiliza los temporizadores, calcula las filas adjudicadas una vez por muestra y obtiene los cuartiles en una llamada. Los bucles restantes representan combinaciones experimentales y repeticiones necesarias; no son bucles anidados sobre todas las filas. El número de ejecuciones medido crece con tamaños × variables × algoritmos × repeticiones × ejecuciones por ronda; reducir ese diseño reduciría evidencia, no la complejidad del algoritmo.

## Resultados del conjunto completo

44.226 filas de entrada y 44.025 seleccionadas por estado; cinco tamaños de proveedor y siete tipos de licitación.

| Agrupación | Algoritmo | Mínimo (ms) | Mediana (ms) | Q25–Q75 (ms) | Pico trazado (MiB) |
| --- | --- | ---: | ---: | ---: | ---: |
| TamanoProveedor | referencia_f2 | 20.764 | 22.118 | 21.263–22.812 | 6.51 |
| TamanoProveedor | iterativa | 22.088 | 23.082 | 22.456–23.473 | 4.55 |
| TamanoProveedor | recursiva | 21.505 | 22.277 | 22.100–23.308 | 4.55 |
| TamanoProveedor | agrupada | 18.168 | 19.024 | 18.318–19.777 | 4.55 |
| TipoLicitacion | referencia_f2 | 23.555 | 24.444 | 24.236–26.895 | 6.51 |
| TipoLicitacion | iterativa | 22.649 | 23.056 | 22.916–23.360 | 4.55 |
| TipoLicitacion | recursiva | 22.422 | 22.924 | 22.806–23.891 | 4.55 |
| TipoLicitacion | agrupada | 20.177 | 20.964 | 20.595–21.791 | 4.55 |

## Interpretación y elección

Se selecciona `tabla_proporciones_agrupada` para el análisis de F3 sobre el conjunto completo: obtuvo la menor mediana en ambas variables y un pico trazado similar al de las otras dos alternativas nuevas, menor que la referencia F2. La mejora frente a F2 es aproximadamente 1,16 veces por tamaño y 1,17 veces por tipo en esta sesión. Esto no implica que pandas sea siempre más rápido ni que toda la ejecución del proyecto mejore en esa proporción.

Con la lectura anterior de 74 columnas, la mejora frente a F2 era de 1,74 y 1,72 veces. Gran parte del costo de la referencia provenía de filtrar varias veces columnas que el cálculo no usa: al leer solo las columnas necesarias, su mediana pasó de ~67 a ~22 ms, y la iterativa y la recursiva quedaron a la par de ella. La agrupada sigue siendo entre un 9 % y un 18 % más rápida que esas dos alternativas.

La ventaja por tipo frente a la iterativa/recursiva es cercana a un 9 %. En muestras pequeñas, las versiones iterativa y recursiva pueden tener menor costo fijo que agrupar. Por ello la elección se limita al volumen y las categorías del estudio, y no demuestra superioridad universal. No se reemplaza automáticamente la función pública F2 ni se introduce un selector dinámico.

El pico similar de las tres alternativas nuevas sugiere que la preparación común pesa más que las diferencias de conteo en esta medición. El filtrado copia todas las columnas recibidas antes de extraer las necesarias; por eso leer solo las columnas del análisis redujo el pico trazado de 40,81 a 6,51 MiB en la referencia y de 26,07 a 4,55 MiB en las alternativas nuevas.

La recursividad no aporta una ventaja sostenida sobre el recorrido iterativo. Su valor en este avance es mostrar descomposición, terminación y combinación correcta de resultados sobre un problema real. No hay cambio de unidad analítica ni nuevos hallazgos causales.

## Complejidad temporal y espacial

Sea N el total de registros de entrada, n los seleccionados, g los grupos y b el bloque base. Con cantidad de columnas fija y hashing de costo esperado constante, filtrar cuesta O(N), preparar resultados O(n) y ordenar grupos O(g log g). El conteo iterativo requiere O(n) tiempo y O(g) memoria; la función completa añade las estructuras de preparación.

Para la recursiva, L = max(1, ceil(n/b)) aproxima las hojas. La profundidad es O(log L). El trabajo es O(n + S), donde S suma las entradas de diccionario combinadas en nodos internos. S tiene cotas O(gL) y O(n log L): para g y b fijos es lineal, pero con alta cardinalidad puede acercarse a O(n log L). La memoria incluye diccionarios parciales, no solo pila; una cota del conteo es O(n + log L).

La variante agrupada y la referencia con tres resultados fijos tienen costo esperado lineal de agrupación, además del ordenamiento de grupos. Las constantes difieren. Las funciones completas requieren memoria auxiliar O(N + n + g) bajo columnas fijas por máscaras, datos filtrados, estructuras de conteo y salida. Las mediciones apoyan una elección práctica, no prueban por sí solas estas cotas.

## Reproducibilidad y límites

El notebook `F3/F3_Algoritmos.ipynb` integra las clases existentes, muestra ejemplos, ejecuta pruebas y consulta evidencia con comprobación de hashes. Puede regenerar las mediciones con `REGENERAR_MEDICIONES = True`. El script `F3/medir_algoritmos.py` guarda tiempos crudos, picos, parámetros, versiones y hashes en `evidencias/F3_algoritmos/`. La ejecución del notebook se registra con `F3/verificar_algoritmos.py`.

Los aportes de lectura (Mauricio) y de limpieza y validación (Naya) están integrados. Quedan para la integración grupal las referencias docentes/académicas, la referencia al foro si corresponde y el informe institucional con revisión del PDF.

## Referencias técnicas

Python Software Foundation. (s. f.-a). *timeit — Measure execution time of small code snippets*. https://docs.python.org/3/library/timeit.html

Python Software Foundation. (s. f.-b). *tracemalloc — Trace memory allocations*. https://docs.python.org/3/library/tracemalloc.html

The pandas development team. (s. f.). *pandas.DataFrame.groupby*. https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
