# Changelog

Registro de los cambios del proyecto **Análisis de ofertas en licitaciones públicas del sector Salud** (MCDI500, Grupo 5), ordenado por fase y fecha. Cada entrada indica la fecha, la descripción, el commit verificable y la justificación técnica del cambio, junto con su impacto en modularidad, rendimiento o documentación.

- Repositorio: <https://github.com/vbravo29/mcdi500-licitaciones-salud>
- Flujo de ramas: el trabajo se integra en `desarrollo` y pasa a `main` mediante *pull request* (merge sin squash), por lo que cada commit listado conserva su hash en ambas ramas.
- Los hashes enlazan al commit en GitHub. Se pueden verificar localmente con `git show <hash>`.

---

## F1 · Definición del problema y entorno reproducible

| Fecha | Descripción | Commit | Justificación técnica | Impacto |
|---|---|---|---|---|
| 2026-09-08 | Creación del repositorio y estructura inicial: carpetas `F1/`, `F2/`, `data/`, `src/`, `evidencias/`, `requirements.txt` y `.gitignore`. | [`bb517b9`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/bb517b9) | Separar datos, código, notebooks y evidencias desde el inicio permite trazar cada fase y reproducir el entorno. | Modularidad, reproducibilidad |
| 2026-09-08 | Ajustes al README y archivo de responsables del código. | [`b11506f`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/b11506f), [`52056cd`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/52056cd), [`fabf83e`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/fabf83e) | Dejar el README como punto de entrada del proyecto. | Documentación |
| 2026-09-11 | Notebook preliminar de validación de datos y metadatos de prueba. | [`a2eb3a8`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/a2eb3a8), [`56a6536`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/56a6536), [`9b53d5e`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/9b53d5e) | Explorar la estructura de los archivos de ChileCompra antes de elegir el conjunto definitivo. | Exploración inicial |
| 2026-09-12 | Incorporación del dataset de licitaciones del sector Salud (marzo de 2026) y documentación de su fuente, formato y unidad de análisis. | [`25f4703`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/25f4703) | Versionar solo el CSV seleccionado garantiza que todos trabajen sobre los mismos datos de origen. | Reproducibilidad, documentación |
| 2026-09-12 | Desarrollo de F1: pruebas de lectura (caso normal, archivo ausente, columnas faltantes, datos vacíos), script `verificar_f1.py` y evidencia de ejecución. Se eliminan archivos en desuso. | [`34d92c2`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/34d92c2) | Comprobar la lectura en casos límite y registrar la ejecución en `evidencias/F1_ejecucion.json` demuestra que F1 corre de inicio a fin. | Validación, reproducibilidad |
| 2026-09-12 | Primer documento de F1 y mapa conceptual. | [`596a0d0`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/596a0d0) | Formalizar el problema y la unidad de análisis antes de transformar datos. | Documentación |

## F2 · Exploración, limpieza y transformación

| Fecha | Descripción | Commit | Justificación técnica | Impacto |
|---|---|---|---|---|
| 2026-09-13 | Notebook de preprocesamiento F2, script `verificar_f2.py` y funciones de limpieza en `src/proyecto.py`. | [`def5aaf`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/def5aaf) | Mover la lógica a `src/` permite reutilizarla y probarla fuera del notebook. | Modularidad |
| 2026-09-13 | Codificación *one-hot* y refactorización de métodos para eliminar duplicación (DRY); se agrega `src/ejecucion.py` para registrar ejecuciones. | [`57ccca6`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/57ccca6) | Un único punto de ejecución y registro evita diferencias entre verificadores. | Modularidad, mantenibilidad |
| 2026-09-11 a 2026-09-16 | Redacción del informe F1-F2, correcciones de formato (Arial 11) y mapa conceptual. | [`c878a33`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/c878a33), [`ef00f72`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/ef00f72), [`116d2bc`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/116d2bc), [`96bffc1`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/96bffc1), [`b213be1`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/b213be1), [`7ea29f0`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/7ea29f0), [`3eae3d0`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/3eae3d0) | Cumplir el formato institucional e incorporar evidencias de ejecución de los notebooks. | Documentación |
| 2026-09-15 | Limpieza de código, diccionario de variables y eliminación del notebook de validación preliminar. | [`cf79f30`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/cf79f30) | Mantener en el repositorio solo artefactos vigentes y documentar cada variable usada. | Mantenibilidad, documentación |
| 2026-09-16 | Registro de decisiones técnicas y alternativas descartadas de F1 y F2 (`docs/DECISIONES_TECNICAS.md`). | [`13fc069`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/13fc069) | Dejar escrito por qué se eligió cada enfoque y qué se descartó, para que las decisiones se puedan revisar. | Documentación, trazabilidad |
| 2026-09-16 | Actualización del mapa conceptual con el flujo reproducible, las decisiones y un glosario visual. | [`fccc770`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/fccc770) | Alinear el mapa conceptual con el flujo real implementado. | Documentación |

## F3 · Núcleo algorítmico, POO y eficiencia

| Fecha | Descripción | Commit | Justificación técnica | Impacto |
|---|---|---|---|---|
| 2026-09-23 | Núcleo orientado a objetos: contrato de columnas, lector, limpiador y validador, con pruebas (`F3/test_nucleo_poo.py`) y archivos de prueba. | [`8087c45`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/8087c45) | Responde a la observación formativa de reorganizar las funciones de F2 en clases con una sola responsabilidad. | Modularidad, validación |
| 2026-09-24 | Separación de `src/proyecto.py` en módulos por responsabilidad (`datos`, `preprocesamiento`, `validacion`, `analisis`, `pipeline`, `entorno`), conservando la compatibilidad con F1 y F2. | [`189f251`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/189f251) | Alta cohesión y bajo acoplamiento: cada módulo se prueba por separado sin cambiar los resultados previos. | Modularidad |
| 2026-09-26 | Cuatro implementaciones equivalentes del cálculo de proporciones (referencia, iterativa, recursiva por división y conquista, agrupada), mediciones con `timeit` y comprobación de que todas entregan el mismo resultado. | [`48e62d3`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/48e62d3) | Elegir el algoritmo con evidencia empírica y no por intuición; la equivalencia con F2 garantiza que optimizar no cambia los resultados. | Rendimiento, validación |
| 2026-09-27 | Ajustes de limpieza y validación en el núcleo POO, con nuevas pruebas. | [`d90111e`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/d90111e) | Cubrir casos de error del validador (por ejemplo, una lista de reglas vacía). | Validación |
| 2026-09-27 | Corrección del código del curso (MCDIA → MCDI) en la portada y los documentos. | [`ab661e4`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/ab661e4) | Responde a una observación formativa sobre la presentación institucional. | Documentación |
| 2026-09-27 | Lectura configurable en `LectorCSV`: selección de columnas, tipos y filas. | [`7f66d24`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/7f66d24) | Leer solo las columnas necesarias reduce el tiempo de lectura y la memoria. | Rendimiento |
| 2026-09-27 | Registro del entorno (versiones de Python y librerías) junto a cada medición. | [`439b69c`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/439b69c) | Las mediciones solo son comparables si se sabe en qué entorno se tomaron. | Reproducibilidad |
| 2026-09-27 | Script que compara tres formas de leer el CSV, con pruebas de equivalencia entre opciones. | [`f1c2a0c`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/f1c2a0c), [`86da721`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/86da721) | Asegurar que cada forma de lectura produce los mismos datos antes de comparar su rendimiento. | Rendimiento, validación |
| 2026-09-27 | Notebook de rendimiento de lectura con mediciones verificadas, integrado luego en `F3_Algoritmos.ipynb`. | [`e5b61c9`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/e5b61c9), [`e41c1fd`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/e41c1fd) | Concentrar la evidencia de F3 en un solo notebook, con un resultado por celda. | Documentación, trazabilidad |
| 2026-09-27 | Aplicación de la lectura de siete columnas en el análisis. | [`7a0ead5`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/7a0ead5) | El flujo completo bajó de 1.199 a 506 ms y el DataFrame leído de 195,7 a 8,9 MiB, sin cambiar los resultados. | Rendimiento (2,4 veces más rápido, 95 % menos memoria) |
| 2026-09-27 | Script de compatibilidad entre versiones, evidencias de validación y documento `F3_VALIDACION_ENTREGA.md`. | [`d9d8227`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/d9d8227) | Demostrar que los resultados se mantienen al cambiar de entorno. | Reproducibilidad, validación |
| 2026-09-27 | Informe de F3 según la pauta de evaluación. | [`d764ee0`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/d764ee0) | Comunicar los avances de F3. | Documentación |
| 2026-09-27 | Gráficos de rendimiento, informe F3 final, limpieza de archivos temporales y creación de `.mailmap`. | [`87b1526`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/87b1526) | Mostrar las mediciones de forma visual y retirar del repositorio los archivos que no forman parte del proyecto. | Documentación, mantenibilidad |
| 2026-09-28 | Unificación de identidades de Git en `.mailmap`. | [`9135329`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/9135329) | Responde a una observación formativa: una misma persona aparecía con varios nombres. `git shortlog -sn` ahora muestra el aporte real de cada integrante. | Trazabilidad |

## F4 · Comunicación de resultados

| Fecha | Descripción | Commit | Justificación técnica | Impacto |
|---|---|---|---|---|
| 2026-10-03 | Notebook `F4_Comunicacion.ipynb` con tres visualizaciones (tamaño de proveedor, tipo de licitación y plazo de cierre), módulo `src/visualizacion.py`, 10 pruebas y evidencia de ejecución. Se agrega Seaborn a `requirements.txt`. | [`5da8f2a`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/5da8f2a) | Reutilizar el flujo validado de F3 y separar la generación de gráficos en un módulo probado. | Modularidad, comunicación |
| 2026-10-03 | Informe final F4 con la plantilla institucional, y ajustes posteriores de fecha y redacción. | [`91e25d2`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/91e25d2), [`76866f2`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/76866f2), [`c48348b`](https://github.com/vbravo29/mcdi500-licitaciones-salud/commit/c48348b) | Integrar en un solo documento las fases F1-F4, los resultados y la trazabilidad de mejoras. | Documentación |

---
