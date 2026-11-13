# TP9 - SmartTicket: Secuencia HU1 (Selección y Cotización)

```mermaid
sequenceDiagram
    actor Espectador
    participant Router as CotizacionRouter
    participant Servicio as CotizacionService
    participant ErepE as EventoRepository
    participant ErepT as EntradaRepository
    participant Evento
    participant Precio as PrecioSector
    participant Manejador as ManejadorExcepciones

    Espectador->>Router: POST /cotizar (evento_id, sector_id, cantidad)
    Router->>Servicio: cotizar(evento_id, sector_id, cantidad)

    alt Escenario 3: cantidad <= 0
        Servicio--)Router: CantidadInvalida
        Router->>Manejador: manejar(CantidadInvalida)
        Manejador-->>Espectador: 400 "Cantidad inválida"
    else cantidad valida
        Servicio->>ErepE: buscar_por_id(evento_id)
        ErepE-->>Servicio: Optional[Evento]

        alt el evento no existe
            Servicio--)Router: EventoNoEncontrado
            Router->>Manejador: manejar(EventoNoEncontrado)
            Manejador-->>Espectador: 404 "Evento no encontrado"
        else el evento existe
            Servicio->>Evento: precio_de(sector_id)

            alt el sector no tiene precio en el evento
                Evento--)Servicio: SectorNoEncontradoEnEvento
                Servicio--)Router: SectorNoEncontradoEnEvento
                Router->>Manejador: manejar(SectorNoEncontradoEnEvento)
                Manejador-->>Espectador: 404 "El sector no tiene precio definido en este evento"
            else el sector tiene precio
                Evento-->>Servicio: PrecioSector
                Servicio->>ErepT: buscar_disponibles(evento_id, sector_id, cantidad)
                ErepT-->>Servicio: entradas disponibles (hasta cantidad)

                alt Escenario 2: disponibles < cantidad
                    Servicio--)Router: CapacidadInsuficiente
                    Router->>Manejador: manejar(CapacidadInsuficiente)
                    Manejador-->>Espectador: 400 "Capacidad insuficiente"
                else Escenario 1: hay disponibilidad
                    Servicio->>Precio: subtotal(cantidad)
                    Precio-->>Servicio: Decimal (ej. 24000)
                    Servicio-->>Router: Cotizacion(total, entrada_ids)
                    Router-->>Espectador: 200 OK (total, entrada_ids)
                end
            end
        end
    end
```

## Lectura del diagrama

- El router solo recibe la petición y devuelve la respuesta (`CotizacionResponse`). No tiene `if` ni cálculos.
- La validación de la cantidad y de la disponibilidad está en `CotizacionService`.
- El orden es: cantidad, evento, **precio del sector** y recién después la disponibilidad. Un sector sin precio en el evento se informa antes de consultar las entradas.
- El subtotal lo calcula `PrecioSector`, que es quien conoce el precio (Information Expert). `Evento.precio_de()` lo busca entre los precios del evento.
- La cotización **no reserva ni modifica** las entradas: solo las identifica. La reserva ocurre al pagar (HU2).
- Los errores son excepciones de dominio. `ManejadorExcepciones` las traduce a HTTP.
- El mensaje del enunciado para estos errores es más largo ("La cantidad de entradas solicitadas debe ser mayor a cero" y "Capacidad insuficiente o entradas no disponibles"). El código usa los textos cortos que se ven en el diagrama; falta confirmar con el docente cuál usar.

## Prerrequisito: alta del evento

Las entradas que cotiza HU1 existen porque el evento las genera al crearse. Este flujo no es una historia del enunciado, pero es el que deja el inventario listo.

```mermaid
sequenceDiagram
    actor Organizador
    participant Router as EventoRouter
    participant Servicio as EventoService
    participant RepoL as LugarRepository
    participant RepoE as EventoRepository
    participant Evento
    participant Manejador as ManejadorExcepciones

    Organizador->>Router: POST /eventos (lugar_id, nombre, fecha, precios)
    Router->>Servicio: crear_evento(lugar_id, nombre, fecha, precios)
    Servicio->>RepoL: buscar_por_id(lugar_id)
    RepoL-->>Servicio: Optional[Lugar]

    alt el lugar no existe
        Servicio--)Router: LugarNoEncontrado
        Router->>Manejador: manejar(LugarNoEncontrado)
        Manejador-->>Organizador: 404 "Lugar no encontrado"
    else el lugar existe
        alt precios repetidos, faltan sectores o sobran sectores ajenos al lugar
            Servicio--)Router: PreciosInvalidos
            Router->>Manejador: manejar(PreciosInvalidos)
            Manejador-->>Organizador: 400 "Debe definirse un precio para cada sector del lugar, sin repetir ni agregar otros"
        else un precio por cada sector del lugar
            Servicio->>Evento: crear Evento con un PrecioSector por sector
            Servicio->>Evento: generar_entradas()
            Note right of Evento: Una Entrada DISPONIBLE con codigo_qr unico por cada lugar fisico de cada sector
            Servicio->>RepoE: guardar(Evento)
            RepoE-->>Servicio: Evento
            Servicio-->>Router: Evento
            Router-->>Organizador: 201 Created (evento con precios)
        end
    end
```

- `Evento.generar_entradas()` aplica Creator: el evento crea sus entradas, una por cada lugar de la capacidad máxima de cada sector.
- `EventoService` verifica que haya exactamente un precio por cada sector del lugar antes de crear nada.
