# Revisión técnica de F3 — 27 de septiembre de 2026

Revisión contra `sumativo-2/sumativo 2.txt`, el avance formativo y la
retroalimentación docente, incluida su aclaración del 22 de septiembre.
El documento Word y su correspondencia final con el notebook quedan fuera de
esta revisión.

## Requisitos técnicos

| Requisito | Evidencia y resultado |
| --- | --- |
| Funciones claras, módulos y flujo verificable | `src/` separa lectura, transformaciones, limpieza, validación y análisis; `src/proyecto.py` conserva la interfaz anterior. |
| Preprocesamiento y conservación de resultados | F1 y F2 se ejecutaron en kernels nuevos sobre copias temporales. Las tablas de proporciones coinciden con las salidas guardadas y ambos CSV regenerados coinciden por SHA-256 con los locales. |
| Casos normales, límites y excepciones | 29 pruebas aprobadas: ocho de algoritmos, 14 de POO y siete de lectura. Se ejecutan también dentro del notebook. |
| Comparación de eficiencia | Cuatro algoritmos y tres opciones de lectura; tiempos con `timeit`, memoria por separado, repeticiones, datos crudos, versiones y hashes. Las mediciones de lectura se regeneraron tras modificar el contrato. |
| Recursividad justificada | `_contar_dividiendo` divide intervalos, termina en bloques de hasta 256 filas y suma conteos parciales. Las secciones 4 y 10 explican terminación, equivalencia y complejidad. No se afirma que sea la alternativa más rápida. |
| Herencia y polimorfismo | `LectorCSV` implementa `LectorDatos`; las reglas implementan `ReglaValidacion`. El validador admite reglas nuevas sin cambiar su coordinación, verificado mediante una regla de prueba. |
| Encapsulamiento | El contrato copia los nombres a una tupla; el limpiador protege su resumen y conserva la entrada; el validador mantiene una colección de reglas y rechaza una lista vacía. |
| Notebook ejecutado y documentado | 32 celdas de código, ejecución completa en un kernel nuevo, pruebas integradas y tablas separadas por propósito. Registro en `evidencias/F3_algoritmos_ejecucion.json`. |
| Repositorio reproducible | F2/F3 organizados, dependencias e instrucciones en README. Los CSV procesados se regeneran y están excluidos de Git, expresamente documentado. |
| Contribuciones individuales | El historial contiene aportes recientes de Víctor, Nayadeth y Mauricio. Los cambios de este cierre aún requieren commit y publicación. |

## Conservación de la primera entrega

`F3/verificar_compatibilidad.py` ejecuta copias temporales de los notebooks y
redirige las exportaciones de F2 a una carpeta temporal. No guarda cambios en
F1, F2 ni en sus registros de ejecución. Compara las dos tablas de proporciones
con las salidas del notebook original y los CSV completos mediante SHA-256.
También contrasta los prefijos de hash visibles en la evidencia anterior:
la tabla del CSV codificado truncaba su hash al mostrarlo.

El resultado y las huellas de los archivos conservados se registran en
`evidencias/F3_compatibilidad.json`. Esta comprobación requiere los dos CSV
locales de F2. No modifica la unidad de observación, los filtros ni los
denominadores del primer entregable.

## Pendientes para la entrega completa

- Cerrar el informe institucional, revisar su correspondencia con las cifras
  actuales del notebook y verificar el PDF exportado. El Word no se modificó.
- Verificar la bibliografía grupal: al menos dos fuentes docentes, dos técnicas
  oficiales y una académica complementaria, con citas y formato APA 7. El
  notebook contiene fuentes técnicas; eso no cubre por sí solo la diversidad
  exigida. No se ha validado la bibliografía del Word en esta revisión.
- Resolver las identidades históricas de Git. Víctor aún aparece con tres
  nombres; también existe el autor `alexander`. No se reasignan autorías ni se
  reescribe el historial sin aclarar su correspondencia. La aclaración final
  del profesor mantiene la observación sobre las identidades de Víctor.
- Publicar los cambios revisados en `desarrollo` y realizar la revisión grupal
  antes de integrar en `main`.

La parte técnica revisada funciona y conserva los resultados anteriores.
El cumplimiento global de la entrega depende todavía del informe, sus fuentes,
la trazabilidad de autores y la publicación del cierre.
