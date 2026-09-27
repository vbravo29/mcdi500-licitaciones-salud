"""Genera el informe Word con portada, índice y el punto II de Sumativa 2."""
from pathlib import Path
import shutil
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

RAIZ = Path(__file__).resolve().parents[1]
PLANTILLA = RAIZ / "docs/informe_f1_f2_grupo_5.docx"
SALIDA = RAIZ / "docs/f3_s02_grupo5.docx"


def reemplazar(p, texto):
    if p.runs:
        p.runs[0].text = texto
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        p.add_run(texto)


def limpiar_cuerpo(doc):
    for p in list(doc.paragraphs[17:]):
        p._element.getparent().remove(p._element)
    for t in list(doc.tables):
        t._element.getparent().remove(t._element)


def agregar_indice(doc):
    p = doc.add_paragraph(style="toc 1")
    r = p.add_run()
    ini = OxmlElement("w:fldChar"); ini.set(qn("w:fldCharType"), "begin")
    ins = OxmlElement("w:instrText"); ins.set(qn("xml:space"), "preserve"); ins.text = ' TOC \\o "1-2" \\h \\z \\u '
    sep = OxmlElement("w:fldChar"); sep.set(qn("w:fldCharType"), "separate")
    r._r.extend([ini, ins, sep])
    entradas = (
        "II. Diseño de soluciones algorítmicas eficientes\t3",
        "    A. Codificación funcional y arquitectura básica del script\t3",
        "    B. Preprocesamiento y transformación del dataset\t4",
        "    C. Validación técnica y verificación del código\t5",
        "    D. Eficiencia y optimización\t6",
        "    E. Diseño estructurado del código\t7",
    )
    for i, entrada in enumerate(entradas):
        if i:
            r._r.append(OxmlElement("w:br"))
        txt = OxmlElement("w:t"); txt.set(qn("xml:space"), "preserve"); txt.text = entrada; r._r.append(txt)
    fin = OxmlElement("w:fldChar"); fin.set(qn("w:fldCharType"), "end"); r._r.append(fin)


def titulo(doc, texto, nivel):
    doc.add_paragraph(texto, style="Título 11" if nivel == 1 else "Título 21")


def parrafo(doc, texto):
    p = doc.add_paragraph(texto)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(6)


def tabla(doc, leyenda, encabezados, filas):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
    rr = p.add_run(leyenda); rr.bold = True; rr.italic = True
    t = doc.add_table(rows=1, cols=len(encabezados)); t.style = "Grid Table 1 Light Accent 1"
    for i, valor in enumerate(encabezados):
        c = t.rows[0].cells[i]; c.text = valor; c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        shd = OxmlElement("w:shd"); shd.set(qn("w:fill"), "24364B"); c._tc.get_or_add_tcPr().append(shd)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in c.paragraphs[0].runs:
            run.bold = True; run.font.color.rgb = RGBColor(255,255,255); run.font.size = Pt(9)
    for n, fila in enumerate(filas, 1):
        cells = t.add_row().cells
        for i, valor in enumerate(fila):
            cells[i].text = str(valor); cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            if n % 2 == 0:
                shd = OxmlElement("w:shd"); shd.set(qn("w:fill"), "F2F5F8"); cells[i]._tc.get_or_add_tcPr().append(shd)
            for run in cells[i].paragraphs[0].runs:
                run.font.size = Pt(9)
    doc.add_paragraph()


def construir():
    shutil.copyfile(PLANTILLA, SALIDA)
    doc = Document(SALIDA); limpiar_cuerpo(doc); p = doc.paragraphs
    portada = {1:"MCDI500 • PROGRAMACIÓN PARA LA CIENCIA DE DATOS",2:"MAGÍSTER EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL",3:"UNIVERSIDAD ANDRÉS BELLO",5:"Análisis de ofertas en licitaciones públicas del sector Salud",6:"Sumativa 2  Avance del proyecto Fase 3",7:"Núcleo algorítmico eficiencia y aplicación de principios de POO",9:"Grupo 5",10:"Víctor Bravo Barrera",11:"Nayadeth Garrido Ibáñez",12:"Mauricio Cid",14:"Docente  Omar Salinas Silva",15:"Fecha  27 de septiembre de 2026"}
    for i, texto in portada.items():
        reemplazar(p[i], texto)

    idx = doc.add_paragraph("Índice de contenidos", style="Title"); idx.alignment = WD_ALIGN_PARAGRAPH.LEFT
    agregar_indice(doc); doc.add_page_break()

    titulo(doc,"II. Diseño de soluciones algorítmicas eficientes",1)
    parrafo(doc,"Esta etapa integra el procesamiento desarrollado en F2 con tres estrategias para calcular la proporción de ofertas ganadoras por tamaño de proveedor y tipo de licitación. El flujo se evaluó sobre las 44.226 filas del reporte del sector Salud de marzo de 2026. Todas las variantes entregan los mismos resultados y se comparan mediante pruebas, mediciones de tiempo y estimaciones de memoria reproducibles.")

    titulo(doc,"A. Codificación funcional y arquitectura básica del script",2)
    parrafo(doc,"El código separa lectura, limpieza, validación y análisis. Las interfaces de F1 y F2 se conservan para no romper los notebooks anteriores. src/analisis.py mantiene tabla_proporciones como referencia y añade las variantes iterativa, recursiva y agrupada. Las tres reciben un DataFrame, una variable de agrupación y el estado administrativo, y devuelven una tabla con conteos, denominadores y porcentajes.")
    parrafo(doc,"La versión iterativa mantiene contadores por grupo. La recursiva divide intervalos de índices y combina diccionarios parciales, con un bloque base configurable de 256 registros. La versión agrupada utiliza operaciones groupby de pandas. Las funciones comparten la preparación de datos y la construcción de la salida, lo que evita repetir validaciones y reglas de negocio.")

    titulo(doc,"B. Preprocesamiento y transformación del dataset",2)
    parrafo(doc,"El pipeline reutiliza el dataset procesado en F2 y conserva las 44.226 observaciones. Comprueba las columnas obligatorias, elimina tres variables completamente vacías, convierte diez variables de fecha, neutraliza 7.613 fechas anómalas del año 1900 y elimina espacios sobrantes en las categorías. También genera oferta_ganadora, licitacion_adjudicada y plazo_cierre_dias. Al eliminar y crear tres variables, el resultado conserva 74 columnas.")
    tabla(doc,"Tabla 1  Transformaciones reutilizadas en F3",("Etapa","Tratamiento","Justificación"),(
        ("Esquema","Cinco columnas obligatorias.","Evita procesar un archivo incompleto."),("Columnas vacías","Exclusión de tres variables 100 % vacías.","No contienen información utilizable."),("Fechas","Conversión a datetime y NaT para 1900.","Calcula plazos sin fechas ficticias."),("Texto","Eliminación de espacios en los extremos.","Unifica etiquetas sin cambiar su significado."),("Variables derivadas","Dos indicadores y un plazo en días.","Facilita las validaciones y el análisis.")))
    parrafo(doc,"No se aplicó escalamiento porque esta etapa compara frecuencias y proporciones, no entrena un modelo. TamanoProveedor conserva la categoría NoClasificado para no asignar artificialmente esas ofertas a otro tamaño empresarial.")

    titulo(doc,"C. Validación técnica y verificación del código",2)
    parrafo(doc,"La verificación combina seis pruebas del núcleo POO con ocho pruebas algorítmicas. Estas incluyen un resultado manual conocido, equivalencia con F2, grupos sin resultados válidos, valores ausentes, categorías reservadas, entradas vacías, columnas ausentes, índices repetidos, bloques recursivos inválidos, particiones aleatorias y el dataset real en sus dos agrupaciones. Las 14 pruebas finalizaron correctamente.")
    tabla(doc,"Tabla 2  Cobertura de verificación",("Caso","Comprobación","Resultado"),(
        ("Normal","Lectura, limpieza, validación y conteo.","Correcto"),("Equivalencia","Referencia, iterativa, recursiva y agrupada.","Correcto"),("Límite","Vacíos, NA, otros estados e índices repetidos.","Correcto"),("Excepción","Columnas ausentes y bloques inválidos.","Controlada"),("Dataset real","TamanoProveedor y TipoLicitacion.","Correcto"),("Total","Seis pruebas POO y ocho algorítmicas.","14 de 14")))
    parrafo(doc,"La trazabilidad queda en F3/test_nucleo_poo.py, F3/test_algoritmos.py, F3/F3_Algoritmos.ipynb y evidencias/F3_algoritmos/. El arnés valida la equivalencia antes de registrar cada medición.")

    titulo(doc,"D. Eficiencia y optimización",2)
    parrafo(doc,"La medición utilizó timeit con siete rondas de tres ejecuciones, orden alternado, calentamiento previo y semilla 2026. Se informa la mediana por llamada. Las muestras anidadas contienen 100, 1.000, 10.000 y 44.226 filas. El tiempo incluye filtrado, preparación, conteo y formato de salida, pero excluye la lectura y limpieza del CSV.")
    tabla(doc,"Tabla 3  Mediana en el conjunto completo en milisegundos",("Agrupación","Referencia F2","Iterativa","Recursiva","Agrupada"),(("TamanoProveedor","66,922","41,857","41,691","38,554"),("TipoLicitacion","68,251","40,716","40,528","39,760")))
    tabla(doc,"Tabla 4  Complejidad y memoria observada",("Implementación","Complejidad temporal","Pico trazado"),(("Referencia F2","O(n)","40,81 MiB"),("Iterativa","O(n)","26,07 MiB"),("Recursiva divide y vencerás","O(n + S), pila O(log L)","26,07 MiB"),("Agrupada con pandas","O(n)","26,07 MiB")))
    parrafo(doc,"Se selecciona tabla_proporciones_agrupada para F3 porque obtuvo la menor mediana en ambas variables y un pico trazado similar al de las otras alternativas nuevas. Frente a la referencia F2, la mejora observada fue de aproximadamente 1,74 veces por tamaño de proveedor y 1,72 veces por tipo de licitación. La ventaja sobre las versiones iterativa y recursiva es menor, por lo que la elección se limita al volumen y las categorías de este estudio.")
    parrafo(doc,"Los picos se midieron con tracemalloc y representan asignaciones rastreadas por Python, no toda la memoria nativa de pandas o NumPy. Por ello se interpretan como una comparación controlada dentro del mismo entorno y no como el consumo total del proceso.")

    titulo(doc,"E. Diseño estructurado del código",2)
    parrafo(doc,"El flujo se organiza en cinco pasos: leer, limpiar, validar, calcular y medir. Cada paso recibe una entrada definida y devuelve un resultado comprobable. src/datos.py y src/pipeline.py concentran la preparación; src/validacion.py aplica las reglas; src/analisis.py contiene las variantes comparables; y F3 separa pruebas, notebook y mediciones. Esta distribución evita mezclar la presentación con la lógica de procesamiento.")
    tabla(doc,"Tabla 5  Flujo y responsabilidades",("Paso","Módulo","Comprobación antes de avanzar"),(("1  Leer","src/datos.py","Archivo, registros y esquema mínimo."),("2  Limpiar","src/pipeline.py","Fechas, texto y variables derivadas."),("3  Validar","src/validacion.py","Seis reglas de calidad superadas."),("4  Calcular","src/analisis.py","Equivalencia de las implementaciones."),("5  Medir","F3/medir_algoritmos.py","Tiempos, memoria, entorno y hashes.")))
    parrafo(doc,"La recursividad divide el intervalo hasta alcanzar bloques pequeños y luego combina resultados parciales. La profundidad es logarítmica respecto del número de bloques. Aunque no entrega una ventaja sostenida frente al recorrido iterativo, demuestra descomposición, terminación y combinación correcta sobre un problema real.")

    for nombre in ("Title","Título 11","Título 21","toc 1","toc 2"):
        if nombre in doc.styles:
            doc.styles[nombre].font.color.rgb = RGBColor(0,0,0)
    upd = OxmlElement("w:updateFields"); upd.set(qn("w:val"), "true"); doc.settings._element.append(upd)
    doc.core_properties.title = "Análisis de ofertas en licitaciones públicas del sector Salud Fase 3"
    doc.save(SALIDA)
    print(SALIDA)


if __name__ == "__main__":
    construir()
