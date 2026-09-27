"""Pruebas unitarias del primer incremento POO de F3."""
from pathlib import Path
import sys
import unittest

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.proyecto import (  # noqa: E402
    ContratoEsquema,
    LectorCSV,
    LimpiadorLicitaciones,
    ReglaValidacion,
    ValidadorDatasetProcesado,
    leer_datos_f1,
    limpiar_datos_f2,
    validar_dataset_procesado,
)


def datos_minimos():
    """Caso pequeño que conserva las reglas relevantes del dataset real."""
    return pd.DataFrame({
        "NroLicitacion": ["1-1-LP26", "2-1-LE26"],
        "TipoLicitacion": [" LP ", "LE"],
        "TamanoProveedor": ["Micro", "Grande"],
        "ResultadoOferta": ["Ganadora", "Perdedora"],
        "EstadoLicitacion": ["Adjudicada", "Adjudicada"],
        "FechaPublicacion": ["2026-03-01", "2026-03-02"],
        "FechaCierre": ["2026-03-11", "2026-03-12"],
        "FechaEstimadaEvaluacionOfertas": ["1900-01-01", "2026-03-13"],
        "LicitacionBaseTipo": [pd.NA, pd.NA],
        "ContratoRenovable": [pd.NA, pd.NA],
        "UnidadTiempoRenovacion": [pd.NA, pd.NA],
    })


class ReglaSiempreValida(ReglaValidacion):
    """Demuestra extensibilidad del validador mediante polimorfismo."""

    nombre = "regla_extension"

    def validar(self, df, filas_esperadas):
        assert len(df) == filas_esperadas


class PruebasNucleoPOO(unittest.TestCase):
    def test_contrato_rechaza_definiciones_invalidas(self):
        with self.assertRaisesRegex(ValueError, "al menos una columna"):
            ContratoEsquema(())
        with self.assertRaisesRegex(ValueError, "duplicadas"):
            ContratoEsquema(("id", "id"))

    def test_lector_rechaza_un_contrato_de_otro_tipo(self):
        with self.assertRaisesRegex(TypeError, "ContratoEsquema"):
            LectorCSV(("id", "valor"))

    def test_lector_aplica_contrato_y_adaptador_conserva_resultado(self):
        ruta = RAIZ / "F3" / "fixtures" / "muestra_valida.csv"
        lector = LectorCSV(ContratoEsquema(("id", "valor")))
        resultado_objeto = lector.leer(ruta)
        resultado_funcion = leer_datos_f1(ruta, ["id", "valor"])
        pd.testing.assert_frame_equal(resultado_objeto, resultado_funcion)

    def test_lector_rechaza_esquema_incompleto(self):
        ruta = RAIZ / "F3" / "fixtures" / "muestra_sin_valor.csv"
        lector = LectorCSV(ContratoEsquema(("id", "valor")))
        with self.assertRaisesRegex(ValueError, "Faltan columnas requeridas"):
            lector.leer(ruta)

    def test_limpiador_encapsula_estado_y_no_muta_entrada(self):
        entrada = datos_minimos()
        original = entrada.copy(deep=True)
        limpiador = LimpiadorLicitaciones()
        salida = limpiador.limpiar(entrada)

        pd.testing.assert_frame_equal(entrada, original)
        self.assertEqual(limpiador.ultima_ejecucion["filas_salida"], 2)
        self.assertEqual(len(limpiador.ultima_ejecucion["columnas_excluidas"]), 3)
        self.assertEqual(salida.loc[0, "TipoLicitacion"], "LP")
        self.assertTrue(pd.isna(salida.loc[0, "FechaEstimadaEvaluacionOfertas"]))
        pd.testing.assert_frame_equal(salida, limpiar_datos_f2(entrada))

    def test_resumen_del_limpiador_es_una_copia_defensiva(self):
        limpiador = LimpiadorLicitaciones()
        limpiador.limpiar(datos_minimos())

        resumen_externo = limpiador.ultima_ejecucion
        resumen_externo["filas_salida"] = 999
        resumen_externo["columnas_excluidas"] = ()

        resumen_interno = limpiador.ultima_ejecucion
        self.assertEqual(resumen_interno["filas_salida"], 2)
        self.assertEqual(len(resumen_interno["columnas_excluidas"]), 3)

    def test_limpiador_rechaza_configuracion_y_entradas_invalidas(self):
        with self.assertRaisesRegex(TypeError, "excluir_vacias"):
            LimpiadorLicitaciones(excluir_vacias="no")
        with self.assertRaisesRegex(TypeError, "DataFrame"):
            LimpiadorLicitaciones().limpiar([])
        with self.assertRaisesRegex(ValueError, "DataFrame vacío"):
            LimpiadorLicitaciones().limpiar(pd.DataFrame())

        sin_columna_clave = datos_minimos().drop(columns="NroLicitacion")
        with self.assertRaisesRegex(KeyError, "columnas clave"):
            LimpiadorLicitaciones().limpiar(sin_columna_clave)

        fecha_invalida = datos_minimos()
        fecha_invalida.loc[0, "FechaPublicacion"] = "fecha imposible"
        with self.assertRaisesRegex(ValueError, "fechas no interpretables"):
            LimpiadorLicitaciones().limpiar(fecha_invalida)

    def test_validador_por_reglas_y_adaptador(self):
        salida = LimpiadorLicitaciones().limpiar(datos_minimos())
        resultado = ValidadorDatasetProcesado().validar(salida, 2)
        self.assertEqual(resultado["estado"], "OK")
        self.assertEqual(resultado["reglas_superadas"], 6)
        self.assertEqual(validar_dataset_procesado(salida, 2)["estado"], "OK")

    def test_validador_acepta_reglas_polimorficas(self):
        salida = LimpiadorLicitaciones().limpiar(datos_minimos())
        resultado = ValidadorDatasetProcesado([ReglaSiempreValida()]).validar(
            salida, 2
        )
        self.assertEqual(resultado["detalle_reglas"], ("regla_extension",))

    def test_validador_distingue_ausencia_de_reglas_de_lista_vacia(self):
        self.assertEqual(len(ValidadorDatasetProcesado().reglas), 6)
        with self.assertRaisesRegex(ValueError, "al menos una regla"):
            ValidadorDatasetProcesado([])

    def test_validador_rechaza_reglas_y_datos_invalidos(self):
        with self.assertRaisesRegex(TypeError, "colección de reglas"):
            ValidadorDatasetProcesado(42)
        with self.assertRaisesRegex(TypeError, "heredar de ReglaValidacion"):
            ValidadorDatasetProcesado([object()])

        validador = ValidadorDatasetProcesado([ReglaSiempreValida()])
        with self.assertRaisesRegex(TypeError, "DataFrame"):
            validador.validar([], 0)
        with self.assertRaisesRegex(AssertionError, "está vacío"):
            validador.validar(pd.DataFrame(), 0)

    def test_validador_detecta_caso_limite(self):
        salida = LimpiadorLicitaciones().limpiar(datos_minimos())
        salida.loc[0, "plazo_cierre_dias"] = -1
        with self.assertRaises(AssertionError):
            ValidadorDatasetProcesado().validar(salida, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
