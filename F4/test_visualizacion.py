"""Pruebas de las visualizaciones de F4: contenido de las figuras y entradas inválidas."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

import matplotlib
if "ipykernel" not in sys.modules:
    matplotlib.use("Agg")  # fuera de Jupyter, las pruebas no abren ventanas
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.analisis import tabla_proporciones_agrupada
from src.visualizacion import (
    FUENTE, formato_numero, grafico_plazos, grafico_proporciones,
    guardar_figura, plazos_por_licitacion,
)


def ofertas():
    """Ofertas de ejemplo: tres licitaciones, dos tipos y resultados conocidos."""
    return pd.DataFrame({
        "NroLicitacion": ["L1", "L1", "L1", "L2", "L2", "L3"],
        "TipoLicitacion": ["Pública", "Pública", "Pública", "Pública", "Pública", "Privada"],
        "TamanoProveedor": ["Grande", "Grande", "Micro", "Micro", "Grande", "Micro"],
        "EstadoLicitacion": ["Adjudicada"] * 6,
        "ResultadoOferta": ["Ganadora", "Ganadora", "Perdedora", "Ganadora", "Perdedora", "Ganadora"],
        "plazo_cierre_dias": [10.0, 10.0, 10.0, 20.0, 20.0, 5.0],
    })


def textos(fig):
    """Reúne los textos visibles de la figura: ejes, anotaciones y notas al pie."""
    eje = fig.axes[0]
    return [t.get_text() for t in eje.texts] + [t.get_text() for t in fig.texts]


class PruebasVisualizacion(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_formato_numero_usa_separadores_locales(self):
        self.assertEqual(formato_numero(18830), "18.830")
        self.assertEqual(formato_numero(66.78, 1), "66,8")

    def test_proporciones_dibuja_una_barra_por_grupo_en_orden(self):
        tabla = tabla_proporciones_agrupada(ofertas(), "TamanoProveedor")
        fig = grafico_proporciones(tabla, "Título de prueba", "Tamaño")
        eje = fig.axes[0]
        barras = [p.get_width() for p in eje.patches]
        self.assertEqual(len(barras), 2)                # sin la fila del total
        self.assertEqual(barras, sorted(barras))        # ordenadas por porcentaje
        self.assertAlmostEqual(max(barras), 66.67, places=2)

    def test_proporciones_incluye_titulo_ejes_leyenda_y_fuente(self):
        tabla = tabla_proporciones_agrupada(ofertas(), "TamanoProveedor")
        fig = grafico_proporciones(tabla, "Título de prueba", "Tamaño")
        eje = fig.axes[0]
        self.assertEqual(eje.get_title(loc="left"), "Título de prueba")
        self.assertTrue(eje.get_xlabel())
        self.assertEqual(eje.get_ylabel(), "Tamaño")
        self.assertIsNotNone(eje.get_legend())
        self.assertTrue(any(FUENTE in texto for texto in textos(fig)))

    def test_proporciones_marca_grupos_con_poco_respaldo(self):
        tabla = tabla_proporciones_agrupada(ofertas(), "TamanoProveedor")
        fig = grafico_proporciones(tabla, "Título", "Tamaño", minimo_ofertas=100)
        leyenda = [t.get_text() for t in fig.axes[0].get_legend().get_texts()]
        self.assertTrue(any("Menos de 100" in texto for texto in leyenda))
        fig = grafico_proporciones(tabla, "Título", "Tamaño", minimo_ofertas=0)
        leyenda = [t.get_text() for t in fig.axes[0].get_legend().get_texts()]
        self.assertFalse(any("Menos de" in texto for texto in leyenda))

    def test_proporciones_no_modifica_la_tabla(self):
        tabla = tabla_proporciones_agrupada(ofertas(), "TamanoProveedor")
        copia = tabla.copy()
        grafico_proporciones(tabla, "Título", "Tamaño", etiquetas={"Micro": "Microempresa"})
        pd.testing.assert_frame_equal(tabla, copia)

    def test_proporciones_rechaza_entradas_invalidas(self):
        tabla = tabla_proporciones_agrupada(ofertas(), "TamanoProveedor")
        with self.assertRaises(ValueError):
            grafico_proporciones(tabla.drop(columns="% Ganadora"), "Título", "Tamaño")
        with self.assertRaises(ValueError):
            grafico_proporciones(tabla.drop(index="All"), "Título", "Tamaño")
        with self.assertRaises(ValueError):
            grafico_proporciones(tabla.loc[["All"]], "Título", "Tamaño")
        with self.assertRaises(ValueError):
            grafico_proporciones(tabla, "Título", "Tamaño", minimo_ofertas=-1)

    def test_plazos_usa_una_fila_por_licitacion(self):
        datos = ofertas()
        copia = datos.copy()
        plazos = plazos_por_licitacion(datos)
        self.assertEqual(len(plazos), 3)
        self.assertEqual(sorted(plazos.plazo_cierre_dias), [5.0, 10.0, 20.0])
        pd.testing.assert_frame_equal(datos, copia)     # la entrada no cambia

    def test_plazos_rechaza_columnas_ausentes_y_datos_inconsistentes(self):
        with self.assertRaises(KeyError):
            plazos_por_licitacion(ofertas().drop(columns="plazo_cierre_dias"))
        inconsistente = ofertas()
        inconsistente.loc[1, "plazo_cierre_dias"] = 99.0   # misma licitación, otro plazo
        with self.assertRaises(ValueError):
            plazos_por_licitacion(inconsistente)
        with self.assertRaises(ValueError):
            grafico_plazos(ofertas().assign(plazo_cierre_dias=float("nan")), "Título")

    def test_grafico_plazos_separa_cajas_y_puntos(self):
        fig = grafico_plazos(ofertas(), "Plazos de prueba", minimo_licitaciones=2)
        eje = fig.axes[0]
        self.assertEqual(eje.get_title(loc="left"), "Plazos de prueba")
        self.assertTrue(eje.get_xlabel())
        self.assertEqual([t.get_text() for t in eje.get_yticklabels()], ["Pública", "Privada"])
        leyenda = [t.get_text() for t in eje.get_legend().get_texts()]
        self.assertIn("Mediana", leyenda)
        self.assertTrue(any("individual" in texto for texto in leyenda))
        self.assertTrue(any("n = 2" in texto for texto in textos(fig)))
        self.assertTrue(any(FUENTE in texto for texto in textos(fig)))

    def test_guardar_figura_crea_el_archivo(self):
        tabla = tabla_proporciones_agrupada(ofertas(), "TamanoProveedor")
        fig = grafico_proporciones(tabla, "Título", "Tamaño")
        with TemporaryDirectory() as temporal:
            ruta = guardar_figura(fig, Path(temporal) / "figuras" / "prueba.png", dpi=50)
            self.assertTrue(ruta.is_file())
            self.assertGreater(ruta.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
