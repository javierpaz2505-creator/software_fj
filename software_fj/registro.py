# -*- coding: utf-8 -*-
"""
registro.py
Configura el archivo de logs. Es el único lugar del programa que escribe
en un archivo, tal como pide el enunciado (archivos solo para eventos y errores).
"""

import logging
import os

# El log se guarda junto a este archivo, sin importar desde dónde se ejecute
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "registro_eventos.log")


def obtener_logger():
    """Devuelve el logger del sistema, creándolo solo la primera vez."""
    logger = logging.getLogger("SoftwareFJ")

    # Si ya tiene manejadores, ya fue configurado: no se duplican los mensajes
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # FileHandler escribe cada mensaje en el archivo (modo "a" = agregar al final)
        manejador = logging.FileHandler(RUTA_LOG, mode="a", encoding="utf-8")

        # Formato de cada línea: fecha y hora | nivel | mensaje
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        manejador.setFormatter(formato)

        logger.addHandler(manejador)

    return logger
