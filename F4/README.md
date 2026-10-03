# Fase 4 — Visualización y comunicación de resultados

Esta fase presenta en tres gráficos los resultados del proyecto y los interpreta frente a la hipótesis del análisis: la proporción de ofertas ganadoras aumenta con el tamaño del proveedor. Reutiliza la lectura, la limpieza, la validación y el cálculo de proporciones de las fases anteriores, sin cambiar sus reglas.

## Archivos

| Archivo | Contenido |
| --- | --- |
| [F4_Comunicacion.ipynb](F4_Comunicacion.ipynb) | Datos, hipótesis, tres gráficos con su interpretación, pruebas y síntesis. |
| [test_visualizacion.py](test_visualizacion.py) | Pruebas de las funciones de visualización: contenido de las figuras y entradas inválidas. |
| [verificar_f4.py](verificar_f4.py) | Ejecución del notebook en un kernel nuevo y registro del resultado. |
| `figuras/` | Imágenes generadas por el notebook; son las que usan el informe final y la presentación. |

Las funciones de los gráficos están en [src/visualizacion.py](../src/visualizacion.py). Cada una recibe datos ya preparados y devuelve la figura, sin leer archivos ni modificar su entrada.

## Gráficos

| Gráfico | Pregunta que responde | Datos |
| --- | --- | --- |
| 1. Ofertas ganadoras según el tamaño del proveedor | ¿Cuánto difiere la proporción entre tamaños? | 44.025 ofertas con resultado válido en procesos adjudicados. |
| 2. Ofertas ganadoras según el tipo de licitación | ¿Cambia la proporción según el tipo de proceso? | Las mismas ofertas; los tipos con menos de 100 ofertas se distinguen visualmente. |
| 3. Plazo de cierre según el tipo de licitación | ¿Se diferencian los tipos en el plazo para ofertar? | 1.864 licitaciones, una observación por proceso. |

Los dos primeros se construyen con Matplotlib y el tercero con Seaborn. Todos incluyen título, ejes rotulados, leyenda y fuente.

## Ejecución

Se requiere el entorno del proyecto con las dependencias de [requirements.txt](../requirements.txt), que desde esta fase incluye `matplotlib` y `seaborn`. Desde la raíz del repositorio:

```powershell
# Instalar o actualizar dependencias
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Pruebas de las visualizaciones
.\.venv\Scripts\python.exe -m unittest F4.test_visualizacion -v

# Ejecución y guardado del notebook
.\.venv\Scripts\python.exe F4\verificar_f4.py
```

El verificador guarda las salidas del notebook, regenera las imágenes de `F4/figuras/` y crea `evidencias/F4_ejecucion.json` con la fecha, la versión de Python, el número de celdas ejecutadas y la huella del notebook.

## Decisiones de diseño

- **Barras horizontales ordenadas** para las proporciones: comparan una misma magnitud entre pocas categorías y dejan espacio para los nombres de los tipos de licitación.
- **Un solo color por gráfico**: el color no codifica categorías; el tono claro identifica los grupos con poco respaldo.
- **Tamaño de cada grupo junto a su porcentaje**: un porcentaje calculado con 2 ofertas no tiene el mismo respaldo que uno calculado con 23.590.
- **Plazos por licitación y no por oferta**: el plazo es un atributo del proceso; contarlo por oferta daría más peso a las licitaciones con más ítems.
- **Puntos en lugar de cajas** para los tipos con menos de 30 licitaciones: una caja con tan pocos datos sugeriría una distribución que no se puede estimar.
