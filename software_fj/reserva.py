# -*- coding: utf-8 -*-
"""
reserva.py
Clase Reserva: une un cliente, un servicio, una duración y un estado.
"""

from entidades import EntidadBase, Cliente
from servicios import Servicio
from excepciones import (ReservaInvalidaError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError, ParametroInvalidoError,
                         CalculoInconsistenteError)
from registro import obtener_logger

log = obtener_logger()


class Reserva(EntidadBase):
    """
    Estados posibles: Pendiente -> Confirmada -> Procesada
    Una reserva Pendiente o Confirmada también puede pasar a Cancelada.
    """

    def __init__(self, cliente, servicio, duracion):
        # Se revisa que lo recibido sea del tipo correcto
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")

        # Encadenamiento de excepciones: se convierte el error técnico de la
        # duración en un error de reserva, pero sin perder el original ("from")
        try:
            servicio.validar_parametros(duracion)
        except ParametroInvalidoError as error:
            raise ReservaInvalidaError("No se puede crear la reserva: duración no válida.") from error

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__costo_final = None
        super().__init__("RES")

    # Solo lectura desde afuera
    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_final(self):
        return self.__costo_final

    def confirmar(self):
        """Pendiente -> Confirmada."""
        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar {self.id}: está {self.__estado}.")
        # El servicio pudo quedar fuera de servicio después de crear la reserva
        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(
                f"No se puede confirmar {self.id}: '{self.__servicio.nombre}' ya no está disponible.")
        self.__estado = "Confirmada"

    def cancelar(self):
        """Pendiente o Confirmada -> Cancelada."""
        if self.__estado in ("Cancelada", "Procesada"):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar {self.id}: ya está {self.__estado}.")
        self.__estado = "Cancelada"

    def procesar(self, impuesto=0.0, descuento=0.0):
        """
        Confirmada -> Procesada. Calcula el costo final.
        También sobrecargado con parámetros opcionales:
            procesar()                 -> sin impuesto ni descuento
            procesar(0.19)             -> con impuesto
            procesar(0.19, 0.10)       -> con impuesto y descuento
        """
        if self.__estado != "Confirmada":
            raise OperacionNoPermitidaError(
                f"No se puede procesar {self.id}: debe estar Confirmada y está {self.__estado}.")

        try:
            costo = self.__servicio.calcular_costo(self.__duracion, impuesto, descuento)
        except (ParametroInvalidoError, CalculoInconsistenteError) as error:
            # Se encadena el error original para saber exactamente qué falló
            raise ReservaInvalidaError(f"No se pudo procesar {self.id}.") from error
        else:
            # Solo si el cálculo salió bien se cambia el estado
            self.__costo_final = costo
            self.__estado = "Procesada"
            return costo
        finally:
            # Se ejecuta siempre, haya salido bien o mal
            log.info(f"Intento de procesar {self.id} terminado (estado: {self.__estado})")

    def describir(self):
        costo = f" | total ${self.__costo_final:,.2f}" if self.__costo_final is not None else ""
        return (f"Reserva {self.id} [{self.__estado}]: {self.__cliente.nombre} -> "
                f"{self.__servicio.nombre} x {self.__duracion}{costo}")
