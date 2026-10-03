"""Ejecuta y guarda el notebook de visualización de F4 en un kernel nuevo."""
from pathlib import Path
import json
import sys

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.ejecucion import ejecutar_notebook


if __name__ == "__main__":
    registro = ejecutar_notebook(
        RAIZ, "F4/F4_Comunicacion.ipynb", "evidencias/F4_ejecucion.json",
        "F4: lectura, limpieza y validación con las clases de F3; tres visualizaciones con interpretación, pruebas de las figuras y exportación a F4/figuras.",
    )
    print(json.dumps(registro, ensure_ascii=False, indent=2))
