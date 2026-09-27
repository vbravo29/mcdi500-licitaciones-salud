"""Versiones de las dependencias y datos del equipo."""
from importlib.metadata import version
import platform
import sys


def versiones_entorno():
    """Registra versiones; falla si falta una dependencia requerida."""
    paquetes = ("numpy", "pandas", "jupyterlab", "ipykernel",
                "nbformat", "nbconvert", "nbclient")
    return {nombre: version(nombre) for nombre in paquetes}


def registro_entorno():
    """Intérprete, sistema y procesador junto a las versiones, para las mediciones."""
    return {
        "python": sys.version,
        "sistema": platform.platform(),
        "procesador": platform.processor(),
        **versiones_entorno(),
    }
