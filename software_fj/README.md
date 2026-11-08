# Software FJ - Sistema de gestión de clientes, servicios y reservas

Proyecto de la Fase 4 del curso Programación (213023), UNAD.
Sistema orientado a objetos, sin base de datos, con manejo avanzado de excepciones.

## Cómo ejecutarlo

```
python main.py
```

Requiere Python 3 (probado con 3.12). No necesita instalar librerías externas.
Cada ejecución agrega los eventos y errores al archivo `registro_eventos.log`.

## Archivos

| Archivo | Qué contiene |
|---|---|
| `main.py` | Programa principal: simula 22 operaciones válidas e inválidas |
| `entidades.py` | Clase abstracta `EntidadBase` y clase `Cliente` (datos privados y validaciones) |
| `servicios.py` | Clase abstracta `Servicio` y sus hijas `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | Clase `Reserva` (estados: Pendiente, Confirmada, Procesada, Cancelada) |
| `gestor.py` | Clase `GestorFJ`: listas internas y operaciones con manejo de errores |
| `excepciones.py` | Excepciones personalizadas (todas heredan de `ErrorFJ`) |
| `registro.py` | Configuración del archivo de logs |

## Conceptos aplicados

- Abstracción: `EntidadBase` y `Servicio` son clases abstractas.
- Herencia y polimorfismo: los tres servicios sobrescriben `validar_parametros`, `calcular_costo_base` y `describir`.
- Encapsulación: atributos privados con propiedades y validaciones.
- Sobrecarga (simulada con parámetros opcionales): `calcular_costo(duracion, impuesto=0.0, descuento=0.0)`.
- Excepciones: personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.
