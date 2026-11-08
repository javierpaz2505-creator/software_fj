# -*- coding: utf-8 -*-
"""
servicios.py
Clase abstracta Servicio y tres servicios especializados que heredan de ella:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
"""

from abc import ABC, abstractmethod

from entidades import EntidadBase
from excepciones import (ServicioInvalidoError, ParametroInvalidoError,
                         CalculoInconsistenteError)


def _es_numero(valor):
    """True si el valor es int o float (y no un booleano, que en Python cuenta como int)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


class Servicio(EntidadBase, ABC):
    """Clase abstracta con lo que tienen en común todos los servicios."""

    def __init__(self, nombre, tarifa, prefijo="SRV"):
        # Validaciones comunes a cualquier servicio
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ServicioInvalidoError("El nombre del servicio debe tener al menos 3 letras.")
        if not _es_numero(tarifa) or tarifa <= 0:
            raise ServicioInvalidoError(f"La tarifa debe ser un número mayor que 0 (recibido: {tarifa!r}).")
        self.__nombre = nombre.strip()
        self.__tarifa = tarifa
        self.__disponible = True
        super().__init__(prefijo)

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tarifa(self):
        return self.__tarifa

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        # Solo se acepta True o False
        if not isinstance(valor, bool):
            raise ParametroInvalidoError("La disponibilidad debe ser True o False.")
        self.__disponible = valor

    # ---------- métodos que cada servicio DEBE sobrescribir (polimorfismo) ----------
    @abstractmethod
    def validar_parametros(self, duracion):
        """Revisa que la duración sirva para este tipo de servicio."""

    @abstractmethod
    def calcular_costo_base(self, duracion):
        """Costo sin impuestos ni descuentos, con la regla propia de cada servicio."""

    @abstractmethod
    def describir(self):
        """Texto que describe el servicio."""

    # ---------- método sobrecargado (simulado con parámetros opcionales) ----------
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """
        Python no tiene sobrecarga como Java, así que se simula con parámetros
        opcionales. Se puede llamar de tres formas:
            calcular_costo(3)               -> costo base
            calcular_costo(3, 0.19)         -> con impuesto
            calcular_costo(3, 0.19, 0.10)   -> con impuesto y descuento
        impuesto y descuento son fracciones: 0.19 significa 19 %.
        """
        # 1. Validar los parámetros
        self.validar_parametros(duracion)
        if not _es_numero(impuesto) or not 0 <= impuesto <= 1:
            raise ParametroInvalidoError(f"El impuesto debe estar entre 0 y 1 (recibido: {impuesto!r}).")
        if not _es_numero(descuento) or not 0 <= descuento < 1:
            raise ParametroInvalidoError(f"El descuento debe estar entre 0 y 1 (recibido: {descuento!r}).")

        # 2. Calcular: primero se descuenta y luego se aplica el impuesto
        costo = self.calcular_costo_base(duracion)
        costo = costo * (1 - descuento) * (1 + impuesto)

        # 3. Comprobar que el resultado tenga sentido
        if costo <= 0:
            raise CalculoInconsistenteError(
                f"El cálculo de '{self.nombre}' dio {costo}, que no es un costo válido.")
        return round(costo, 2)


class ReservaSala(Servicio):
    """Reserva de salas. Se cobra por hora más un valor fijo de limpieza."""

    LIMPIEZA = 20000       # cargo fijo por limpieza
    HORAS_MAXIMAS = 8      # una sala no se reserva por más de 8 horas seguidas

    def __init__(self, nombre, tarifa_hora, capacidad):
        # Se valida lo propio de la sala ANTES de llamar al constructor padre
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or not 1 <= capacidad <= 200:
            raise ServicioInvalidoError(f"La capacidad debe ser un entero entre 1 y 200 (recibido: {capacidad!r}).")
        self.__capacidad = capacidad
        super().__init__(nombre, tarifa_hora)

    @property
    def capacidad(self):
        return self.__capacidad

    def validar_parametros(self, duracion):
        if not _es_numero(duracion) or not 1 <= duracion <= self.HORAS_MAXIMAS:
            raise ParametroInvalidoError(
                f"La sala se reserva de 1 a {self.HORAS_MAXIMAS} horas (recibido: {duracion!r}).")

    def calcular_costo_base(self, duracion):
        return self.tarifa * duracion + self.LIMPIEZA

    def describir(self):
        return (f"Sala {self.id}: {self.nombre} | capacidad {self.capacidad} personas | "
                f"${self.tarifa:,.0f} por hora + ${self.LIMPIEZA:,.0f} de limpieza")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos. Se cobra por día más un seguro del 5 %."""

    SEGURO = 0.05
    DIAS_MAXIMOS = 30

    def __init__(self, nombre, tarifa_dia):
        super().__init__(nombre, tarifa_dia)

    def validar_parametros(self, duracion):
        # Los días deben ser enteros
        if not isinstance(duracion, int) or isinstance(duracion, bool) or not 1 <= duracion <= self.DIAS_MAXIMOS:
            raise ParametroInvalidoError(
                f"El equipo se alquila de 1 a {self.DIAS_MAXIMOS} días enteros (recibido: {duracion!r}).")

    def calcular_costo_base(self, duracion):
        alquiler = self.tarifa * duracion
        return alquiler + alquiler * self.SEGURO

    def describir(self):
        return (f"Equipo {self.id}: {self.nombre} | ${self.tarifa:,.0f} por día "
                f"+ {self.SEGURO:.0%} de seguro")


class AsesoriaEspecializada(Servicio):
    """Asesoría por horas. El valor cambia según el nivel del asesor."""

    # Factor que multiplica la tarifa según el nivel
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}
    HORAS_MAXIMAS = 6

    def __init__(self, nombre, tarifa_hora, nivel):
        if not isinstance(nivel, str) or nivel.lower() not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel de asesor desconocido: {nivel!r}. Opciones: {', '.join(self.NIVELES)}.")
        self.__nivel = nivel.lower()
        super().__init__(nombre, tarifa_hora)

    @property
    def nivel(self):
        return self.__nivel

    def validar_parametros(self, duracion):
        if not _es_numero(duracion) or not 1 <= duracion <= self.HORAS_MAXIMAS:
            raise ParametroInvalidoError(
                f"La asesoría dura de 1 a {self.HORAS_MAXIMAS} horas (recibido: {duracion!r}).")

    def calcular_costo_base(self, duracion):
        return self.tarifa * self.NIVELES[self.nivel] * duracion

    def describir(self):
        return (f"Asesoría {self.id}: {self.nombre} | nivel {self.nivel} | "
                f"${self.tarifa:,.0f} por hora x {self.NIVELES[self.nivel]}")
