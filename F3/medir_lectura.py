"""Compara formas de leer el CSV: todas las columnas, solo las necesarias y con tipos."""
import argparse
from datetime import datetime, timezone
from functools import partial
import hashlib
import json
from pathlib import Path
import random
import sys

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from F3.medir_algoritmos import medir_memoria, medir_tiempos, resumir_medicion
from src.analisis import tabla_proporciones
from src.datos import (
    COLUMNAS_ANALISIS, TIPOS_ANALISIS, ContratoEsquema, LectorCSV, sha256_archivo,
)
from src.entorno import registro_entorno
from src.pipeline import LimpiadorLicitaciones
from src.validacion import ValidadorDatasetProcesado

RUTA = RAIZ / "data/raw/licitaciones_salud_marzo_2026.csv"
SHA256_CSV = "490d9209a10d387011d481b72b7891f26e997974ec2cf9dfc518aa4a08552232"
CONTRATO = ContratoEsquema(("TamanoProveedor", "TipoLicitacion", "ResultadoOferta", "EstadoLicitacion"))
GRUPOS = ("TamanoProveedor", "TipoLicitacion")
DERIVADAS = ("oferta_ganadora", "licitacion_adjudicada", "plazo_cierre_dias")


def sha256_codigo(ruta):
    """Huella de un archivo de texto con saltos de línea normalizados a LF.

    git en Windows (core.autocrlf) entrega CRLF; sin normalizar, la misma
    versión del código tendría otra huella en cada sistema operativo.
    """
    return hashlib.sha256(Path(ruta).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def crear_lectores():
    """Las tres opciones comparten contrato, separador y codificación."""
    return {
        "actual": LectorCSV(CONTRATO),
        "solo_columnas": LectorCSV(CONTRATO, columnas=COLUMNAS_ANALISIS),
        "columnas_y_tipos": LectorCSV(CONTRATO, columnas=COLUMNAS_ANALISIS, tipos=TIPOS_ANALISIS),
    }


def flujo_completo(lector, ruta):
    """Lectura, limpieza y proporciones: el uso real de la lectura en F3."""
    limpio = LimpiadorLicitaciones().limpiar(lector.leer(ruta))
    return limpio, [tabla_proporciones(limpio, grupo) for grupo in GRUPOS]


def comprobar_equivalencia(lectores, ruta):
    """Antes de medir: mismas columnas necesarias, validación y proporciones idénticas.

    Se compara después de limpiar porque la limpieza normaliza los textos a
    ``string``; al leer, la opción con tipos entrega ``category``.
    """
    columnas = [*COLUMNAS_ANALISIS, *DERIVADAS]
    resultados = {}
    for nombre, lector in lectores.items():
        raw = lector.leer(ruta)
        limpio = LimpiadorLicitaciones().limpiar(raw)
        ValidadorDatasetProcesado().validar(limpio, len(raw))
        resultados[nombre] = (limpio, [tabla_proporciones(limpio, grupo) for grupo in GRUPOS])
    referencia, tablas_referencia = resultados["actual"]
    filas = []
    for nombre, (limpio, tablas) in resultados.items():
        pd.testing.assert_frame_equal(limpio[columnas], referencia[columnas])
        for tabla, esperada in zip(tablas, tablas_referencia):
            pd.testing.assert_frame_equal(tabla, esperada)
        filas.append({"opcion": nombre, "filas": len(limpio), "columnas_limpias": len(limpio.columns),
                      "columnas_necesarias": "iguales", "validacion": "OK", "proporciones": "iguales"})
    return filas


def medir_opciones(llamadas, repeticiones, azar):
    """Tiempo sin tracemalloc (una ejecución por ronda) y memoria por separado."""
    tiempos = medir_tiempos(llamadas, repeticiones, 1, azar)
    resumenes = {}
    for nombre, llamada in llamadas.items():
        resumen = resumir_medicion(nombre, tiempos[nombre], medir_memoria(llamada))
        resumenes[nombre] = {"opcion": resumen.pop("algoritmo"), **resumen}
    return resumenes


def medir(lectores, ruta, tamanos=(1000, 10000, None), repeticiones=7, semilla=2026):
    """Mide lectura por tamaño y el flujo completo sobre todas las filas."""
    if repeticiones < 1:
        raise ValueError("Se requiere al menos una repetición.")
    azar = random.Random(semilla)
    filas = []
    for n in tamanos:
        llamadas = {nombre: partial(lector.leer, ruta, filas=n) for nombre, lector in lectores.items()}
        tamanos_df = {}
        for nombre, llamada in llamadas.items():
            datos = llamada()  # Calentamiento de la caché de disco y tamaño del resultado.
            tamanos_df[nombre] = (len(datos), len(datos.columns), int(datos.memory_usage(deep=True).sum()))
            del datos
        for nombre, resumen in medir_opciones(llamadas, repeticiones, azar).items():
            filas_df, columnas_df, memoria_df = tamanos_df[nombre]
            filas.append({"etapa": "lectura", "filas": filas_df, "columnas": columnas_df,
                          **resumen, "memoria_dataframe_bytes": memoria_df})
    llamadas = {nombre: partial(flujo_completo, lector, ruta) for nombre, lector in lectores.items()}
    tamanos_df = {}
    for nombre, llamada in llamadas.items():
        limpio, _ = llamada()
        tamanos_df[nombre] = (len(limpio), len(limpio.columns), int(limpio.memory_usage(deep=True).sum()))
        del limpio
    for nombre, resumen in medir_opciones(llamadas, repeticiones, azar).items():
        filas_df, columnas_df, memoria_df = tamanos_df[nombre]
        filas.append({"etapa": "flujo_completo", "filas": filas_df, "columnas": columnas_df,
                      **resumen, "memoria_dataframe_bytes": memoria_df})
    return filas


def ejecutar(salida=None, repeticiones=7):
    """Comprueba el archivo y la equivalencia, mide y guarda CSV y metadatos JSON."""
    salida = Path(salida) if salida else RAIZ / "F3/mediciones_lectura"
    # Comprobar el destino y el archivo antes de invertir tiempo en el experimento.
    salida.mkdir(parents=True, exist_ok=True)
    if sha256_archivo(RUTA) != SHA256_CSV:
        raise ValueError("El CSV no coincide con la copia utilizada en F2 y F3.")
    lectores = crear_lectores()
    equivalencia = comprobar_equivalencia(lectores, RUTA)
    filas = medir(lectores, RUTA, repeticiones=repeticiones)
    registro = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        **registro_entorno(),
        "raw_sha256": SHA256_CSV,
        "datos_sha256": sha256_codigo(RAIZ / "src/datos.py"),
        "medicion_sha256": sha256_codigo(Path(__file__)),
        "medir_algoritmos_sha256": sha256_codigo(RAIZ / "F3/medir_algoritmos.py"),
        "columnas_analisis": list(COLUMNAS_ANALISIS), "tipos_analisis": TIPOS_ANALISIS,
        "semilla": 2026, "repeticiones": repeticiones, "ejecuciones_por_repeticion": 1,
        "repeticiones_memoria": 3,
        "alcance": "Lectura del CSV con LectorCSV (1.000, 10.000 filas y archivo completo) y flujo completo: lectura, limpieza y proporciones por tamaño de proveedor y tipo de licitación.",
        "memoria": "memoria_dataframe_bytes: memory_usage(deep=True) del resultado. Pico: asignaciones rastreadas con tracemalloc; no es RSS ni incluye todos los búferes internos del lector de pandas.",
        "tiempo": "timeit sin tracemalloc; GC desactivado durante cada ronda; una ejecución por ronda con orden alternado por semilla y una lectura previa de calentamiento.",
        "equivalencia": equivalencia,
        "mediciones": filas,
    }
    (salida / "mediciones.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tabla = pd.DataFrame(filas).drop(columns=["tiempos_ms", "picos_trazados_bytes"])
    tabla.to_csv(salida / "resumen.csv", index=False)
    return tabla


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path)
    parser.add_argument("--repeticiones", type=int, default=7)
    args = parser.parse_args()
    print(ejecutar(args.salida, args.repeticiones).to_string(index=False))
