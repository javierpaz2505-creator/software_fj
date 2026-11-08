# -*- coding: utf-8 -*-
"""
main.py
Programa principal de Software FJ.
Simula operaciones completas (válidas e inválidas) para demostrar que el
sistema sigue funcionando aunque ocurran errores.

Cómo ejecutarlo:  python main.py
Los errores y eventos quedan en el archivo registro_eventos.log
"""

from gestor import GestorFJ
from registro import obtener_logger, RUTA_LOG

log = obtener_logger()
numero_operacion = 0


def operacion(titulo):
    """Imprime el encabezado numerado de cada operación simulada."""
    global numero_operacion
    numero_operacion += 1
    print(f"\nOPERACIÓN {numero_operacion}: {titulo}")
    log.info(f"--- Operación {numero_operacion}: {titulo} ---")


def main():
    print("=" * 70)
    print("SOFTWARE FJ - Sistema de gestión de clientes, servicios y reservas")
    print("=" * 70)
    log.info("===== Inicio de la simulación =====")

    fj = GestorFJ()

    # ---------------- CLIENTES ----------------
    operacion("Registro válido de cliente")
    laura = fj.registrar_cliente("Laura Gómez", "1061234567", "laura.gomez@correo.com", "3101234567")

    operacion("Registro válido de otro cliente")
    carlos = fj.registrar_cliente("Carlos Pérez", 1098765432, "carlos.perez@correo.com", "3209876543")

    operacion("Registro inválido: correo sin arroba")
    fj.registrar_cliente("Marta Ruiz", "52123456", "marta.ruiz.correo.com", "3001112233")

    operacion("Registro inválido: documento con letras y teléfono corto")
    fj.registrar_cliente("Pedro Díaz", "12AB56", "pedro@correo.com", "311")

    operacion("Registro inválido: documento repetido")
    fj.registrar_cliente("Laura Duplicada", "1061234567", "otra@correo.com", "3101112222")

    # ---------------- SERVICIOS ----------------
    operacion("Creación correcta de una sala")
    sala = fj.crear_servicio("sala", "Sala de Reuniones A", 45000, 12)

    operacion("Creación correcta de un alquiler de equipo")
    proyector = fj.crear_servicio("equipo", "Proyector HD", 60000)

    operacion("Creación correcta de una asesoría")
    asesoria = fj.crear_servicio("asesoria", "Asesoría en Python", 80000, "senior")

    operacion("Creación incorrecta: tarifa negativa")
    fj.crear_servicio("sala", "Sala Fantasma", -5000, 10)

    operacion("Creación incorrecta: faltan parámetros (error encadenado)")
    fj.crear_servicio("asesoria", "Asesoría incompleta", 70000)

    operacion("Creación incorrecta: tipo de servicio que no existe")
    fj.crear_servicio("catering", "Servicio de comida", 30000)

    # ---------------- RESERVAS ----------------
    operacion("Reserva exitosa: confirmar y procesar con IVA y descuento")
    reserva1 = fj.crear_reserva(laura.id, sala.id, 3)
    fj.confirmar_reserva(reserva1)
    fj.procesar_reserva(reserva1, 0.19, 0.10)

    operacion("Reserva fallida: duración fuera del rango de la sala (error encadenado)")
    fj.crear_reserva(carlos.id, sala.id, 20)

    operacion("Reserva fallida: cliente que no existe")
    fj.crear_reserva("CLI-999", proyector.id, 2)

    operacion("Reserva fallida: servicio fuera de servicio")
    proyector.disponible = False   # simula que el equipo está en mantenimiento
    fj.crear_reserva(carlos.id, proyector.id, 2)
    proyector.disponible = True    # vuelve a quedar disponible

    operacion("Reserva exitosa de asesoría y luego cancelación")
    reserva2 = fj.crear_reserva(carlos.id, asesoria.id, 2)
    fj.cancelar_reserva(reserva2)

    operacion("Operación no permitida: cancelar una reserva ya cancelada")
    fj.cancelar_reserva(reserva2)

    operacion("Operación no permitida: procesar una reserva sin confirmar")
    reserva3 = fj.crear_reserva(laura.id, proyector.id, 5)
    fj.procesar_reserva(reserva3, 0.19)

    operacion("Descuento inválido al procesar (error encadenado)")
    fj.confirmar_reserva(reserva3)
    fj.procesar_reserva(reserva3, 0.19, 1.5)

    operacion("Error inesperado: confirmar un objeto que no es una reserva")
    fj.confirmar_reserva(None)

    # ---------------- DEMOSTRACIONES ----------------
    operacion("Método sobrecargado: tres formas de calcular el costo de la sala")
    print(f"   calcular_costo(3)              -> ${sala.calcular_costo(3):>12,.2f}")
    print(f"   calcular_costo(3, 0.19)        -> ${sala.calcular_costo(3, 0.19):>12,.2f}")
    print(f"   calcular_costo(3, 0.19, 0.10)  -> ${sala.calcular_costo(3, 0.19, 0.10):>12,.2f}")

    operacion("Polimorfismo: un solo ciclo, cada servicio responde a su manera")
    for servicio in fj.servicios:
        # Misma llamada para todos; el resultado depende del tipo de servicio
        print(f"   {servicio.describir()}")
        print(f"      costo de 2 unidades con IVA 19 %: ${servicio.calcular_costo(2, 0.19):,.2f}")

    # ---------------- RESUMEN ----------------
    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    print(f"Operaciones simuladas:   {numero_operacion}")
    print(f"Acciones exitosas:       {fj.operaciones_ok}")
    print(f"Errores controlados:     {fj.operaciones_fallidas}")
    print(f"Clientes registrados:    {len(fj.clientes)}")
    print(f"Servicios creados:       {len(fj.servicios)}")
    print(f"Reservas guardadas:      {len(fj.reservas)}")
    for reserva in fj.reservas:
        print(f"   - {reserva.describir()}")
    print(f"\nEl programa terminó sin interrupciones. Log en: {RUTA_LOG}")
    log.info("===== Fin de la simulación =====")


if __name__ == "__main__":
    main()
