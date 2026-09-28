"""Verifica F1/F2 en copias temporales sin reescribir la primera entrega."""
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import sys

import nbformat

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.datos import sha256_archivo
from src.ejecucion import ejecutar_notebook


def verificar():
    """Ejecuta copias, contrasta resultados y guarda evidencia solo si coinciden."""
    notebooks = [next((RAIZ / fase).glob('*.ipynb')) for fase in ('F1', 'F2')]
    csvs = sorted((RAIZ / 'data/processed').glob('*.csv'))
    if len(csvs) != 2:
        raise ValueError('Se requieren los dos CSV procesados de F2 para comparar.')
    protegidos = notebooks + csvs + [
        RAIZ / 'data/raw/licitaciones_salud_marzo_2026.csv',
        RAIZ / 'evidencias/F1_ejecucion.json', RAIZ / 'evidencias/F2_ejecucion.json',
    ]
    originales = {str(p.relative_to(RAIZ)): sha256_archivo(p) for p in protegidos}
    ejecuciones = []
    # Dentro del proyecto para que los notebooks encuentren src/ en sus ancestros.
    with TemporaryDirectory(prefix='.f3-compat-', dir=RAIZ) as temporal:
        destino = Path(temporal)
        for ruta in notebooks:
            original = nbformat.read(ruta, as_version=4)
            copia = nbformat.read(ruta, as_version=4)
            if ruta.parent.name == 'F2':
                for celda in copia.cells:
                    if celda.cell_type == 'code':
                        celda.source = celda.source.replace(
                            'raiz / "data" / "processed"',
                            f'Path({str(destino / "processed")!r})',
                        )
            nbformat.write(copia, destino / ruta.name)
            registro = ejecutar_notebook(
                destino, ruta.name, f'{ruta.parent.name}.json',
                'Copia temporal; exportaciones de F2 aisladas de la primera entrega.',
            )
            ejecuciones.append({
                'fase': ruta.parent.name,
                'celdas_codigo_ejecutadas': registro['celdas_codigo_ejecutadas'],
                'kernel_nuevo': registro['kernel_nuevo'], 'errores': registro['errores'],
            })
            if ruta.parent.name == 'F2':
                ejecutado = nbformat.read(destino / ruta.name, as_version=4)
                indice = next(i for i, c in enumerate(original.cells)
                              if c.cell_type == 'code' and 'tabla_resumen_tamano =' in c.source)
                def tablas_texto(celda):
                    return [o['data']['text/plain'] for o in celda.outputs
                            if 'data' in o and 'text/plain' in o['data']]
                esperadas = tablas_texto(original.cells[indice])
                assert len(esperadas) == 2, 'Faltan las dos tablas de referencia guardadas.'
                assert tablas_texto(ejecutado.cells[indice]) == esperadas, 'Cambiaron las proporciones de F2.'
                salida_original = json.dumps([c.get('outputs', []) for c in original.cells])
                for csv in csvs:
                    huella = originales[str(csv.relative_to(RAIZ))]
                    # pandas truncó el hash codificado en la tabla de la entrega.
                    # Se contrasta el prefijo visible y, por separado, los 64
                    # caracteres del hash local frente al CSV regenerado.
                    assert huella[:40] in salida_original, f'{csv.name}: difiere del prefijo documentado en F2.'
                    assert sha256_archivo(destino / 'processed' / csv.name) == huella, f'Cambio en {csv.name}.'
        for ruta, huella in originales.items():
            assert sha256_archivo(RAIZ / ruta) == huella, f'Se modificó {ruta}.'
    evidencia = {
        'fecha_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version, 'ejecuciones': ejecuciones,
        'tablas_proporciones_f2_identicas': True,
        'csv_regenerados_identicos_a_csv_locales': True,
        'prefijos_hash_coinciden_con_evidencia_f2': True,
        'archivos_originales_sin_cambios': originales,
        'datos_codigo_sha256': sha256_archivo(RAIZ / 'src/datos.py'),
    }
    (RAIZ / 'evidencias/F3_compatibilidad.json').write_text(
        json.dumps(evidencia, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    return evidencia


if __name__ == '__main__':
    print(json.dumps(verificar(), ensure_ascii=False, indent=2))
