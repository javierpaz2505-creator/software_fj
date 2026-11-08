# -*- coding: utf-8 -*-
"""
entidades.py
Clase abstracta EntidadBase (entidades generales del sistema) y la clase Cliente.
"""

import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError


class EntidadBase(ABC):
    """
    Clase abstracta: representa cualquier entidad del sistema (cliente,
    servicio o reserva). No se puede crear un objeto directamente de ella
    porque tiene un método abstracto.
    """

    # Diccionario compartido que lleva la cuenta de ids por tipo de entidad
    _contadores = {}

    def __init__(self, prefijo):
        # Suma uno al contador de este tipo (CLI, SRV o RES)
        EntidadBase._contadores[prefijo] = EntidadBase._contadores.get(prefijo, 0) + 1
        # Id legible, por ejemplo CLI-001
        self._id = f"{prefijo}-{EntidadBase._contadores[prefijo]:03d}"

    @property
    def id(self):
        """El id solo se puede leer, no cambiar (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe explicar cómo se describe a sí misma."""


class Cliente(EntidadBase):
    """Cliente de Software FJ. Sus datos personales son privados y se validan."""

    def __init__(self, nombre, documento, correo, telefono):
        # Cada asignación pasa por su setter, que valida el dato.
        # Si algo está mal, se lanza ClienteInvalidoError y el objeto no se crea.
        self.nombre = nombre
        self.__documento = self._validar_documento(documento)
        self.correo = correo
        self.telefono = telefono
        # El id se asigna al final: un cliente inválido no gasta número de id
        super().__init__("CLI")

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise ClienteInvalidoError("El nombre debe ser un texto.")
        valor = valor.strip()
        # Solo letras y espacios, mínimo 3 caracteres
        if len(valor) < 3 or not all(letra.isalpha() or letra == " " for letra in valor):
            raise ClienteInvalidoError(
                f"Nombre inválido: '{valor}'. Use solo letras (mínimo 3).")
        self.__nombre = valor

    # ---------- documento (solo lectura) ----------
    @staticmethod
    def _validar_documento(valor):
        valor = str(valor).strip()
        # Solo dígitos, entre 6 y 10
        if not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise ClienteInvalidoError(
                f"Documento inválido: '{valor}'. Debe tener de 6 a 10 dígitos.")
        return valor

    @property
    def documento(self):
        """El documento se puede consultar pero no modificar."""
        return self.__documento

    # ---------- correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str):
            raise ClienteInvalidoError("El correo debe ser un texto.")
        valor = valor.strip()
        # Forma básica: algo@dominio.algo, sin espacios
        if not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", valor):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self.__correo = valor

    # ---------- teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        # Celular colombiano: 10 dígitos que empiezan por 3
        if not (valor.isdigit() and len(valor) == 10 and valor.startswith("3")):
            raise ClienteInvalidoError(
                f"Teléfono inválido: '{valor}'. Debe tener 10 dígitos y empezar por 3.")
        self.__telefono = valor

    def describir(self):
        # Se oculta casi todo el documento por privacidad
        return (f"Cliente {self.id}: {self.nombre} | "
                f"Doc: ******{self.documento[-3:]} | {self.correo}")
