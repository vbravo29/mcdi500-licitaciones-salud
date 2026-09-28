# Fase 3 — Algoritmos y programación orientada a objetos

Esta fase compara algoritmos para calcular la proporción de ofertas ganadoras por tamaño de proveedor y tipo de licitación, y formas de leer el CSV. Utiliza el dataset de F2 y una estructura de clases para la lectura, limpieza y validación de los datos.

El análisis considera ofertas de procesos adjudicados. Cada fila representa una oferta por ítem; los porcentajes se calculan sobre las ofertas con resultado válido de cada grupo.

## Archivos

| Archivo | Contenido |
| --- | --- |
| [F3_Algoritmos.ipynb](F3_Algoritmos.ipynb) | Desarrollo del análisis, ejemplos, pruebas, mediciones y conclusiones de algoritmos (secciones 1–11) y lectura (sección 12). |
| [test_algoritmos.py](test_algoritmos.py) | Pruebas de equivalencia entre algoritmos y casos límite. |
| [test_nucleo_poo.py](test_nucleo_poo.py) | Pruebas de lectura, limpieza y validación mediante clases. |
| [test_lectura.py](test_lectura.py) | Pruebas de la lectura configurable y de la equivalencia entre opciones de lectura. |
| [medir_algoritmos.py](medir_algoritmos.py) | Comparación de tiempos de ejecución y memoria de los algoritmos. |
| [medir_lectura.py](medir_lectura.py) | Comparación de tiempos y memoria de tres formas de leer el CSV. |
| [verificar_algoritmos.py](verificar_algoritmos.py) | Ejecución del notebook en un kernel nuevo y registro del resultado. |
| [verificar_compatibilidad.py](verificar_compatibilidad.py) | Ejecución temporal de F1/F2 y comparación de sus resultados sin sobrescribirlos. |
| `fixtures/` | Archivos de ejemplo utilizados en las pruebas de lectura. |
| `mediciones_lectura/` | Mediciones de lectura: `resumen.csv` y `mediciones.json`. |

## Organización del código

La implementación se encuentra en `src/`:

| Módulo | Responsabilidad |
| --- | --- |
| [datos.py](../src/datos.py) | Contrato de esquema, lector abstracto, lector CSV, exportación y huellas SHA-256. |
| [preprocesamiento.py](../src/preprocesamiento.py) | Transformación de fechas, categorías y variables derivadas. |
| [pipeline.py](../src/pipeline.py) | Coordinación de la limpieza y registro de su última ejecución. |
| [validacion.py](../src/validacion.py) | Reglas de calidad y validación del dataset. |
| [analisis.py](../src/analisis.py) | Exploración, frecuencias y cálculo de proporciones. |

`LectorCSV` implementa la interfaz de `LectorDatos`. `LimpiadorLicitaciones` conserva un resumen de la limpieza sin modificar el DataFrame de entrada. `ValidadorDatasetProcesado` aplica reglas que comparten la interfaz `ReglaValidacion`.

Los notebooks de F1 y F2 mantienen sus importaciones desde `src/proyecto.py`. Las nuevas alternativas de cálculo se importan desde `src/analisis.py`.

## Ejecución

Se requiere el entorno Python del proyecto, las dependencias de [requirements.txt](../requirements.txt) y el archivo `data/raw/licitaciones_salud_marzo_2026.csv`. La configuración del entorno está descrita en el [README principal](../README.md#preparación-del-entorno).

Ejecutar los siguientes comandos desde la raíz del repositorio, en este orden:

```powershell
# Pruebas de algoritmos, clases y lectura
.\.venv\Scripts\python.exe -m unittest F3.test_algoritmos F3.test_nucleo_poo F3.test_lectura -v

# Mediciones de tiempo y memoria
.\.venv\Scripts\python.exe F3\medir_algoritmos.py
.\.venv\Scripts\python.exe F3\medir_lectura.py

# Ejecución y guardado del notebook
.\.venv\Scripts\python.exe F3\verificar_algoritmos.py
```

Las mediciones de algoritmos se guardan en `evidencias/F3_algoritmos/` y las de lectura en `F3/mediciones_lectura/`: `resumen.csv` contiene las estadísticas y `mediciones.json` incluye las observaciones individuales, los parámetros, las versiones y las huellas de los archivos utilizados.

El verificador guarda las salidas del notebook y genera `evidencias/F3_algoritmos_ejecucion.json`. El notebook comprueba que las mediciones correspondan al dataset y al código actuales. Si cambia `src/analisis.py` o `F3/medir_algoritmos.py`, es necesario repetir las mediciones de algoritmos; si cambia `src/datos.py`, `F3/medir_lectura.py` o `F3/medir_algoritmos.py`, las de lectura. También pueden regenerarse desde el notebook con `REGENERAR_MEDICIONES = True` y `REGENERAR_MEDICIONES_LECTURA = True`.

## Comparación de algoritmos

Se comparan cuatro implementaciones:

- **Referencia F2:** cálculo original mediante filtros y agrupaciones.
- **Iterativa:** acumulación de conteos por grupo en un diccionario.
- **Recursiva:** división de registros en bloques y combinación de conteos parciales.
- **Agrupada:** cálculo mediante una agrupación por categoría y resultado.

Las pruebas comprueban que las alternativas producen los mismos resultados. La comparación de rendimiento utiliza distintos tamaños de entrada e incluye el filtrado, las conversiones, el conteo y la construcción de la tabla. La lectura del CSV y la limpieza se realizan antes de medir.

En las mediciones guardadas, la variante agrupada obtuvo la menor mediana de tiempo para el dataset completo en ambas variables. Se utiliza en el análisis de F3; la función de F2 conserva su implementación. La interpretación de los tiempos, la complejidad y los límites de la comparación se desarrolla en el notebook.

La memoria se mide por separado con `tracemalloc`. El pico registrado corresponde a las asignaciones rastreadas durante el cálculo, no a la memoria total del proceso.

## Comparación de lectura

Se comparan tres configuraciones de `LectorCSV`: la lectura actual de todas las columnas, solo las siete columnas necesarias para limpiar, validar y calcular proporciones, y esas columnas con tipos `category` definidos al leer. Antes de medir se comprueba que los datos limpios, la validación y las proporciones sean idénticos a la lectura actual.

En las mediciones guardadas, leer solo las columnas necesarias con tipos hace unas 2,5 veces más rápido el flujo de lectura, limpieza y proporciones, y reduce cerca de un 95 % la memoria del DataFrame leído. Se recomienda para el análisis de F3; F1 y F2 mantienen la lectura completa, que sigue siendo el comportamiento por defecto.

## Validación y documentación

El notebook contiene 32 celdas de código: 24 de algoritmos y 8 de lectura. La suite integrada ejecuta 29 pruebas: ocho de algoritmos, 14 de POO y siete de lectura. `evidencias/F3_algoritmos_ejecucion.json` registra la ejecución completa en un kernel nuevo y la huella del notebook guardado. El notebook presenta por separado la preparación de datos, los casos de prueba, las proporciones, los tiempos y la memoria, con las explicaciones correspondientes a cada resultado.

- [Decisiones técnicas](../docs/DECISIONES_TECNICAS.md): criterios de implementación y alternativas evaluadas.
- [Análisis de algoritmos](../docs/F3_APORTE_ALGORITMOS.md): sección técnica preparada para el informe.
- [Evidencias de rendimiento](../evidencias/F3_algoritmos/): resultados reproducibles del experimento de algoritmos.
- [Mediciones de lectura](mediciones_lectura/): resultados reproducibles del experimento de lectura.

## Pendientes

La [revisión contra la guía](../docs/F3_VALIDACION_ENTREGA.md) detalla las
evidencias y los límites de la validación. Para comprobar la conservación de la
primera entrega, con los dos CSV de F2 disponibles localmente:

```powershell
.\.venv\Scripts\python.exe F3\verificar_compatibilidad.py
```

El resultado queda en `evidencias/F3_compatibilidad.json`. Las exportaciones de
comprobación se generan en una carpeta temporal y se eliminan al terminar.

- Completar el informe grupal y su bibliografía docente, técnica y académica.
- Revisar su correspondencia con el notebook y el PDF final.
- Resolver las identidades históricas de Git señaladas en la revisión.
- Publicar el cierre revisado en `desarrollo` e integrarlo en `main`.
