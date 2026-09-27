"""Ejecuta y guarda el notebook de lectura en un kernel nuevo."""
from pathlib import Path
import json
import sys

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.ejecucion import ejecutar_notebook


if __name__ == "__main__":
    registro = ejecutar_notebook(
        RAIZ, "F3/F3_Lectura.ipynb", "F3/mediciones_lectura/ejecucion.json",
        "Aporte de lectura: tres opciones de LectorCSV, equivalencia de datos limpios y proporciones, mediciones con hashes verificados.",
    )
    print(json.dumps(registro, ensure_ascii=False, indent=2))
