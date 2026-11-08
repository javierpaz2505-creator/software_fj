# -*- coding: utf-8 -*-
"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.

Todas heredan de ErrorFJ. Así, en cualquier parte del programa se puede
atrapar "cualquier error propio del sistema" con un solo except ErrorFJ,
o atrapar un error específico cuando se necesite un trato distinto.
"""


class ErrorFJ(Exception):
    """Error general del sistema. Es la clase padre de todas las demás."""


class ClienteInvalidoError(ErrorFJ):
    """Se lanza cuando los datos de un cliente no pasan las validaciones."""


class ServicioInvalidoError(ErrorFJ):
    """Se lanza cuando un servicio se intenta crear con datos incorrectos."""


class ParametroInvalidoError(ErrorFJ):
    """Se lanza cuando un parámetro (duración, impuesto, descuento) no sirve."""


class ServicioNoDisponibleError(ErrorFJ):
    """Se lanza cuando se pide un servicio que está fuera de servicio."""


class ReservaInvalidaError(ErrorFJ):
    """Se lanza cuando una reserva no se puede crear o procesar."""


class OperacionNoPermitidaError(ErrorFJ):
    """Se lanza cuando se pide algo que el estado actual no permite."""


class CalculoInconsistenteError(ErrorFJ):
    """Se lanza cuando un cálculo de costos da un resultado que no tiene sentido."""
