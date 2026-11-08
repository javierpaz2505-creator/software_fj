# -*- coding: utf-8 -*-
"""
gestor.py
Clase GestorFJ: guarda clientes, servicios y reservas en listas internas
(no hay base de datos) y ejecuta cada operación con manejo de errores.
Ninguna operación detiene el programa: todo error se registra y se sigue.
"""

from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import (ErrorFJ, ClienteInvalidoError, ServicioInvalidoError)
from registro import obtener_logger

log = obtener_logger()


class GestorFJ:
    """Administra todo el sistema de Software FJ."""

    # Tipos de servicio que se pueden crear y la clase que corresponde a cada uno
    TIPOS_SERVICIO = {
        "sala": ReservaSala,
        "equipo": AlquilerEquipo,
        "asesoria": AsesoriaEspecializada,
    }

    def __init__(self):
        # Listas internas: aquí vive toda la información
        self.clientes = []
        self.servicios = []
        self.reservas = []
        # Contadores para el resumen final
        self.operaciones_ok = 0
        self.operaciones_fallidas = 0

    # ------------------------------------------------------------------
    # Métodos de apoyo
    # ------------------------------------------------------------------
    def _exito(self, mensaje):
        """Anota una operación exitosa en pantalla y en el log."""
        self.operaciones_ok += 1
        print(f"   [OK] {mensaje}")
        log.info(mensaje)

    def _fallo(self, mensaje, error):
        """Anota una operación fallida. Si el error tiene una causa, también la registra."""
        self.operaciones_fallidas += 1
        print(f"   [ERROR] {mensaje}: {error}")
        log.error(f"{mensaje}: {error}")
        # __cause__ existe cuando el error se encadenó con "raise ... from ..."
        if error.__cause__ is not None:
            print(f"           causa original -> {error.__cause__}")
            log.error(f"   causa original: {error.__cause__}")

    def buscar_cliente(self, id_cliente):
        for cliente in self.clientes:
            if cliente.id == id_cliente:
                return cliente
        raise ClienteInvalidoError(f"No existe un cliente con id {id_cliente}.")

    def buscar_servicio(self, id_servicio):
        for servicio in self.servicios:
            if servicio.id == id_servicio:
                return servicio
        raise ServicioInvalidoError(f"No existe un servicio con id {id_servicio}.")

    # ------------------------------------------------------------------
    # Clientes
    # ------------------------------------------------------------------
    def registrar_cliente(self, nombre, documento, correo, telefono):
        """try / except / else / finally completo."""
        try:
            # No se permiten dos clientes con el mismo documento
            for existente in self.clientes:
                if existente.documento == str(documento).strip():
                    raise ClienteInvalidoError(f"Ya existe un cliente con el documento {documento}.")
            cliente = Cliente(nombre, documento, correo, telefono)
        except ClienteInvalidoError as error:
            self._fallo("Registro de cliente rechazado", error)
            return None
        except Exception as error:  # cualquier error que no se haya previsto
            self._fallo("Error inesperado al registrar cliente", error)
            return None
        else:
            # Solo se ejecuta si el try salió sin errores
            self.clientes.append(cliente)
            self._exito(f"Cliente registrado -> {cliente.describir()}")
            return cliente
        finally:
            # Se ejecuta siempre
            log.info("Fin del intento de registro de cliente")

    # ------------------------------------------------------------------
    # Servicios
    # ------------------------------------------------------------------
    def _construir_servicio(self, tipo, argumentos):
        """Crea el servicio del tipo pedido. Traduce errores técnicos a errores del sistema."""
        if tipo not in self.TIPOS_SERVICIO:
            raise ServicioInvalidoError(
                f"Tipo de servicio desconocido: {tipo!r}. Opciones: {', '.join(self.TIPOS_SERVICIO)}.")
        try:
            return self.TIPOS_SERVICIO[tipo](*argumentos)
        except TypeError as error:
            # Faltan o sobran parámetros: se encadena el error original
            raise ServicioInvalidoError(
                f"Parámetros incompletos o de más para crear el servicio '{tipo}'.") from error

    def crear_servicio(self, tipo, *argumentos):
        """Ejemplo: crear_servicio("sala", "Sala A", 45000, 12)"""
        try:
            servicio = self._construir_servicio(tipo, argumentos)
        except ErrorFJ as error:
            self._fallo("Creación de servicio rechazada", error)
            return None
        except Exception as error:
            self._fallo("Error inesperado al crear servicio", error)
            return None
        else:
            self.servicios.append(servicio)
            self._exito(f"Servicio creado -> {servicio.describir()}")
            return servicio
        finally:
            log.info("Fin del intento de creación de servicio")

    # ------------------------------------------------------------------
    # Reservas
    # ------------------------------------------------------------------
    def crear_reserva(self, id_cliente, id_servicio, duracion):
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)
            reserva = Reserva(cliente, servicio, duracion)
        except ErrorFJ as error:
            self._fallo("Reserva rechazada", error)
            return None
        except Exception as error:
            self._fallo("Error inesperado al crear reserva", error)
            return None
        else:
            self.reservas.append(reserva)
            self._exito(f"Reserva creada -> {reserva.describir()}")
            return reserva
        finally:
            log.info("Fin del intento de creación de reserva")

    def confirmar_reserva(self, reserva):
        try:
            reserva.confirmar()
        except ErrorFJ as error:
            self._fallo("Confirmación rechazada", error)
            return False
        except Exception as error:
            # Por ejemplo, si llega None en lugar de una reserva
            self._fallo("Error inesperado al confirmar", error)
            return False
        else:
            self._exito(f"Reserva confirmada -> {reserva.describir()}")
            return True

    def cancelar_reserva(self, reserva):
        try:
            reserva.cancelar()
        except ErrorFJ as error:
            self._fallo("Cancelación rechazada", error)
            return False
        except Exception as error:
            self._fallo("Error inesperado al cancelar", error)
            return False
        else:
            self._exito(f"Reserva cancelada -> {reserva.describir()}")
            return True

    def procesar_reserva(self, reserva, impuesto=0.0, descuento=0.0):
        try:
            costo = reserva.procesar(impuesto, descuento)
        except ErrorFJ as error:
            self._fallo("Procesamiento rechazado", error)
            return None
        except Exception as error:
            self._fallo("Error inesperado al procesar", error)
            return None
        else:
            self._exito(f"Reserva procesada -> {reserva.describir()}")
            return costo
