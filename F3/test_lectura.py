"""Pruebas de las opciones de lectura: compatibilidad F1/F2 y equivalencia de datos."""
from pathlib import Path
import sys
import unittest

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from F3.medir_lectura import CONTRATO, RUTA, comprobar_equivalencia, crear_lectores
from src.datos import COLUMNAS_ANALISIS, TIPOS_ANALISIS, ContratoEsquema, LectorCSV, leer_datos_f1

FIXTURES = RAIZ / "F3" / "fixtures"


class PruebasLectura(unittest.TestCase):
    def test_lectura_por_defecto_conserva_f1(self):
        ruta = FIXTURES / "muestra_valida.csv"
        resultado = LectorCSV(ContratoEsquema(("id", "valor"))).leer(ruta)
        pd.testing.assert_frame_equal(resultado, leer_datos_f1(ruta, ["id", "valor"]))

    def test_columnas_seleccionadas_en_orden_del_archivo(self):
        lector = LectorCSV(ContratoEsquema(("valor",)), columnas=("valor", "id"))
        resultado = lector.leer(FIXTURES / "muestra_valida.csv")
        self.assertEqual(list(resultado.columns), ["id", "valor"])

    def test_tipos_definidos_al_leer(self):
        lector = LectorCSV(ContratoEsquema(("valor",)), columnas=("valor",), tipos={"valor": "category"})
        resultado = lector.leer(FIXTURES / "muestra_valida.csv")
        self.assertIsInstance(resultado["valor"].dtype, pd.CategoricalDtype)

    def test_columna_inexistente_informa_contrato(self):
        lector = LectorCSV(ContratoEsquema(("id",)), columnas=("id", "valor"))
        with self.assertRaisesRegex(ValueError, "Faltan columnas requeridas: valor"):
            lector.leer(FIXTURES / "muestra_sin_valor.csv")

    def test_columnas_deben_incluir_contrato(self):
        with self.assertRaisesRegex(ValueError, "omiten requeridas del contrato: valor"):
            LectorCSV(ContratoEsquema(("id", "valor")), columnas=("id",))

    def test_filas_limita_la_lectura(self):
        datos = LectorCSV(CONTRATO, columnas=COLUMNAS_ANALISIS, tipos=TIPOS_ANALISIS).leer(RUTA, filas=100)
        self.assertEqual(datos.shape, (100, len(COLUMNAS_ANALISIS)))

    def test_dataset_real_opciones_equivalentes(self):
        # Falla con AssertionError si alguna opción altera columnas o proporciones.
        filas = comprobar_equivalencia(crear_lectores(), RUTA)
        self.assertEqual([f["opcion"] for f in filas], ["actual", "solo_columnas", "columnas_y_tipos"])
        self.assertEqual({f["filas"] for f in filas}, {44226})


if __name__ == "__main__":
    unittest.main(verbosity=2)
