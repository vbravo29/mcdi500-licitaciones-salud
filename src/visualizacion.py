"""Visualizaciones analíticas de F4: proporciones de ofertas ganadoras y plazos de cierre.

Cada función recibe datos ya preparados por las clases de lectura, limpieza y análisis,
y devuelve la figura de Matplotlib. Ninguna lee archivos ni modifica su entrada.
"""
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import MatplotlibDeprecationWarning
from matplotlib.patches import Patch

FUENTE = "Fuente: elaboración propia con datos abiertos de ChileCompra, sector Salud, marzo de 2026."
COLOR_PRINCIPAL = "#1F4E79"
COLOR_BAJO_RESPALDO = "#9DB7D5"
COLOR_REFERENCIA = "#B03A2E"
COLOR_TEXTO = "#1F2933"

# Etiquetas breves para los ejes; los datos conservan los nombres oficiales.
ETIQUETAS_TIPO = {
    "Licitación Pública Menor a 100 UTM (L1)": "Pública menor a 100 UTM (L1)",
    "Licitación Pública Entre 100 y 1000 UTM (LE)": "Pública de 100 a 1.000 UTM (LE)",
    "Licitación Pública Mayor 1000 UTM (LP)": "Pública mayor a 1.000 UTM (LP)",
    "Licitación Pública Mayor a 5000 (LR)": "Pública mayor a 5.000 UTM (LR)",
    "Licitación Privada entre 100 y 1000 UTM.": "Privada de 100 a 1.000 UTM",
    "Licitación Privada Mayor a 1000 UTM": "Privada mayor a 1.000 UTM",
    "Licitación Privada Mayor a 5000 (I2)": "Privada mayor a 5.000 UTM (I2)",
}
ETIQUETAS_TAMANO = {"NoClasificado": "No clasificado"}


def formato_numero(valor, decimales=0):
    """Formatea con punto de miles y coma decimal, como en el informe."""
    texto = f"{valor:,.{decimales}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def _aplicar_estilo(ax):
    """Estilo común: ejes discretos y texto legible, sin elementos decorativos."""
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#9AA5B1")
    ax.tick_params(colors=COLOR_TEXTO, labelsize=9)
    ax.xaxis.label.set_color(COLOR_TEXTO)
    ax.yaxis.label.set_color(COLOR_TEXTO)


def _agregar_fuente(fig, nota=None):
    """Escribe la nota metodológica y la fuente bajo el gráfico."""
    texto = FUENTE if nota is None else f"{nota}\n{FUENTE}"
    fig.text(0.01, 0.01, texto, ha="left", va="bottom", fontsize=7.5, color="#52606D")


def grafico_proporciones(tabla, titulo, etiqueta_grupo, etiquetas=None, minimo_ofertas=100):
    """Barras horizontales con el porcentaje de ofertas ganadoras por grupo.

    ``tabla`` es la salida de ``tabla_proporciones_agrupada``: una fila por grupo y la
    fila ``All`` con el total. Los grupos con menos de ``minimo_ofertas`` ofertas válidas
    se dibujan en un tono más claro, porque su porcentaje tiene poco respaldo.
    """
    requeridas = {"All", "% Ganadora"}
    if not isinstance(tabla, pd.DataFrame) or not requeridas.issubset(tabla.columns):
        raise ValueError("tabla debe contener las columnas 'All' y '% Ganadora'.")
    if "All" not in tabla.index:
        raise ValueError("tabla debe incluir la fila 'All' con el total.")
    if isinstance(minimo_ofertas, bool) or minimo_ofertas < 0:
        raise ValueError("minimo_ofertas debe ser un número no negativo.")
    grupos = tabla.drop(index="All")
    grupos = grupos.loc[grupos["All"] > 0].sort_values("% Ganadora")
    if grupos.empty:
        raise ValueError("No hay grupos con ofertas válidas para graficar.")
    total = float(tabla.loc["All", "% Ganadora"])
    etiquetas = etiquetas or {}
    nombres = [etiquetas.get(nombre, nombre) for nombre in grupos.index]
    bajo_respaldo = grupos["All"] < minimo_ofertas
    colores = [COLOR_BAJO_RESPALDO if bajo else COLOR_PRINCIPAL for bajo in bajo_respaldo]

    fig, ax = plt.subplots(figsize=(7.6, 0.5 * len(grupos) + 1.7))
    barras = ax.barh(nombres, grupos["% Ganadora"], color=colores, height=0.62)
    for barra, porcentaje, ofertas in zip(barras, grupos["% Ganadora"], grupos["All"]):
        # Los valores se alinean en una columna a la derecha para no cruzar la línea del total.
        ax.text(103, barra.get_y() + barra.get_height() / 2,
                f"{formato_numero(porcentaje, 1)} %  (n = {formato_numero(ofertas)})",
                va="center", ha="left", fontsize=8.5, color=COLOR_TEXTO)
    linea = ax.axvline(total, color=COLOR_REFERENCIA, linestyle="--", linewidth=1.2)
    ax.set_xlim(0, 140)
    ax.set_xticks(range(0, 101, 20))
    ax.set_xlabel("Ofertas ganadoras (% de las ofertas con resultado válido)", fontsize=9.5)
    ax.set_ylabel(etiqueta_grupo, fontsize=9.5)
    ax.set_title(titulo, fontsize=11, fontweight="bold", loc="left", color=COLOR_TEXTO)
    leyenda = [linea]
    textos = [f"Total: {formato_numero(total, 1)} %"]
    if bajo_respaldo.any():
        leyenda.append(Patch(color=COLOR_BAJO_RESPALDO))
        textos.append(f"Menos de {formato_numero(minimo_ofertas)} ofertas válidas")
    ax.legend(leyenda, textos, loc="upper left", bbox_to_anchor=(0, -0.2), ncol=2,
              frameon=False, fontsize=8.5, borderaxespad=0)
    _aplicar_estilo(ax)
    _agregar_fuente(fig, "Procesos adjudicados; n = ofertas con resultado válido de cada grupo.")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    return fig


def plazos_por_licitacion(df):
    """Devuelve una fila por licitación con su tipo y su plazo de cierre en días.

    El plazo es un atributo del proceso y se repite en todas sus ofertas; resumirlo por
    oferta daría más peso a las licitaciones con más ítems y oferentes.
    """
    requeridas = ("NroLicitacion", "TipoLicitacion", "plazo_cierre_dias")
    faltantes = [columna for columna in requeridas if columna not in df.columns]
    if faltantes:
        raise KeyError(f"Faltan columnas para los plazos: {faltantes}")
    unicos = df.loc[:, list(requeridas)].drop_duplicates()
    if unicos["NroLicitacion"].duplicated().any():
        raise ValueError("Una licitación tiene más de un tipo o plazo; revisar antes de graficar.")
    return unicos.dropna(subset=["plazo_cierre_dias"]).reset_index(drop=True)


def grafico_plazos(df, titulo, etiquetas=None, minimo_licitaciones=30):
    """Diagrama de caja del plazo de cierre por tipo de licitación.

    Los tipos con menos de ``minimo_licitaciones`` procesos se muestran solo como puntos:
    una caja con tan pocos datos sugeriría una distribución que no se puede estimar.
    """
    plazos = plazos_por_licitacion(df)
    if plazos.empty:
        raise ValueError("No hay licitaciones con plazo de cierre para graficar.")
    etiquetas = etiquetas or {}
    plazos["Tipo"] = plazos["TipoLicitacion"].astype(str).map(lambda nombre: etiquetas.get(nombre, nombre))
    resumen = plazos.groupby("Tipo")["plazo_cierre_dias"].agg(["median", "size"])
    orden = resumen.sort_values("median", ascending=False).index.tolist()
    con_caja = resumen.index[resumen["size"] >= minimo_licitaciones]

    fig, ax = plt.subplots(figsize=(7.6, 0.52 * len(orden) + 1.7))
    cajas = plazos.loc[plazos["Tipo"].isin(con_caja)]
    if not cajas.empty:
        with warnings.catch_warnings():
            # seaborn 0.13 aún pasa a Matplotlib un argumento que Matplotlib 3.11 marca
            # como obsoleto; el aviso no depende de este proyecto y se silencia solo aquí.
            warnings.simplefilter("ignore", MatplotlibDeprecationWarning)
            sns.boxplot(data=cajas, x="plazo_cierre_dias", y="Tipo", order=orden, ax=ax,
                        color=COLOR_BAJO_RESPALDO, width=0.55, linewidth=1.1,
                        medianprops={"color": COLOR_PRINCIPAL, "linewidth": 2},
                        flierprops={"marker": "o", "markersize": 3, "markerfacecolor": "#52606D",
                                    "markeredgecolor": "none", "alpha": 0.6})
    puntos = plazos.loc[~plazos["Tipo"].isin(con_caja)]
    if not puntos.empty:
        # swarmplot separa los puntos coincidentes de forma determinista (sin azar).
        sns.swarmplot(data=puntos, x="plazo_cierre_dias", y="Tipo", order=orden, ax=ax,
                      color=COLOR_PRINCIPAL, size=5)
    limite = plazos["plazo_cierre_dias"].max()
    for posicion, tipo in enumerate(orden):
        ax.text(limite * 1.04, posicion, f"n = {formato_numero(resumen.loc[tipo, 'size'])}",
                va="center", ha="left", fontsize=8.5, color=COLOR_TEXTO)
    ax.set_xlim(0, limite * 1.18)
    ax.set_xlabel("Plazo entre publicación y cierre (días)", fontsize=9.5)
    ax.set_ylabel("Tipo de licitación", fontsize=9.5)
    ax.set_title(titulo, fontsize=11, fontweight="bold", loc="left", color=COLOR_TEXTO)
    leyenda = [Patch(facecolor=COLOR_BAJO_RESPALDO, edgecolor="#52606D"),
               plt.Line2D([], [], color=COLOR_PRINCIPAL, linewidth=2)]
    textos = ["Rango intercuartílico", "Mediana"]
    if not puntos.empty:
        leyenda.append(plt.Line2D([], [], marker="o", linestyle="", color=COLOR_PRINCIPAL, markersize=5.5))
        textos.append(f"Licitación individual (n < {minimo_licitaciones})")
    ax.legend(leyenda, textos, loc="upper left", bbox_to_anchor=(0, -0.17), ncol=3,
              frameon=False, fontsize=8.5, borderaxespad=0, columnspacing=1.2)
    ax.grid(axis="x", color="#D9E2EC", linewidth=0.6)
    ax.set_axisbelow(True)
    _aplicar_estilo(ax)
    _agregar_fuente(fig, "Una observación por licitación; n = número de licitaciones de cada tipo.")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    return fig


def guardar_figura(fig, ruta, dpi=200):
    """Guarda la figura en PNG con fondo blanco y crea la carpeta si no existe."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=dpi, facecolor="white")
    return ruta
