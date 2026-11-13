# TP9 - SmartTicket: Secuencia HU2 (Pago y Emisión de Entradas)

```mermaid
sequenceDiagram
    actor Espectador
    participant Router as PagoRouter
    participant Servicio as PagoService
    participant RepoC as ClienteRepository
    participant RepoE as EntradaRepository
    participant Entrada
    participant Venta
    participant Pasarela as PasarelaPago
    participant RepoV as VentaRepository
    participant Manejador as ManejadorExcepciones

    Espectador->>Router: POST /iniciar-pago (cliente_id, entrada_ids, tarjeta)
    Note over Router,Pasarela: get_pasarela (Depends) entrega la PasarelaPago al servicio
    Router->>Servicio: iniciar_pago(cliente_id, entrada_ids, DatosTarjeta)
    Servicio->>RepoC: buscar_por_id(cliente_id)
    RepoC-->>Servicio: Optional[Cliente]

    alt el cliente no existe
        Servicio--)Router: ClienteNoEncontrado
        Router->>Manejador: manejar(ClienteNoEncontrado)
        Manejador-->>Espectador: 404 "Cliente no encontrado"
    else el cliente existe
        Servicio->>RepoE: buscar_por_ids(entrada_ids)
        RepoE-->>Servicio: entradas

        alt Escenario 3: faltan o se repiten ids, o alguna entrada no esta disponible
            Note right of Servicio: Primero compara la cantidad de entradas encontradas con los ids pedidos
            Servicio->>Entrada: esta_disponible() de cada entrada
            Entrada-->>Servicio: false
            Servicio--)Router: EntradaNoDisponible
            Router->>Manejador: manejar(EntradaNoDisponible)
            Manejador-->>Espectador: 409 "Los lugares seleccionados ya no se encuentran disponibles"
            Note over Servicio,Pasarela: Se aborta ANTES de consultar a la pasarela
        else las entradas son de distintos eventos
            Servicio--)Router: EntradasDeDistintosEventos
            Router->>Manejador: manejar(EntradasDeDistintosEventos)
            Manejador-->>Espectador: 400 "Las entradas deben pertenecer a un mismo evento"
        else todas disponibles y de un mismo evento
            Servicio->>Entrada: reservar()
            Note right of Entrada: En memoria: DISPONIBLE pasa a RESERVADA
            Servicio->>RepoE: reservar(entradas)
            Note right of RepoE: UPDATE condicional (WHERE estado = DISPONIBLE) y control de rowcount

            alt otro pago se adelanto: rowcount distinto de la cantidad de entradas
                RepoE--)Servicio: EntradaNoDisponible (rollback)
                Servicio--)Router: EntradaNoDisponible
                Router->>Manejador: manejar(EntradaNoDisponible)
                Manejador-->>Espectador: 409 "Los lugares seleccionados ya no se encuentran disponibles"
                Note over Servicio,Pasarela: Tampoco se consulta a la pasarela
            else reserva confirmada en la base (commit)
                Servicio->>Venta: crear Venta PENDIENTE con las entradas
                Servicio->>Venta: calcular_total()
                Venta->>Entrada: precio() de cada entrada
                Note right of Entrada: Entrada.evento.precio_de(sector_id).precio
                Entrada-->>Venta: Decimal
                Venta-->>Servicio: Decimal (ej. 24000)
                Servicio->>Pasarela: procesar_pago(DatosTarjeta, total)
                Pasarela-->>Servicio: RespuestaPago

                alt Escenario 2: Rechazado
                    Servicio->>Entrada: liberar()
                    Note right of Entrada: RESERVADA vuelve a DISPONIBLE
                    Servicio->>RepoE: guardar(entradas)
                    Note over Servicio,RepoV: La venta no se guarda
                    Servicio--)Router: PagoDenegado
                    Router->>Manejador: manejar(PagoDenegado)
                    Manejador-->>Espectador: 402 "Pago denegado"
                else Escenario 1: Aprobado
                    Servicio->>Venta: confirmar_pago()
                    Note right of Venta: PENDIENTE pasa a PAGADA
                    Servicio->>Entrada: emitir()
                    Note right of Entrada: RESERVADA pasa a EMITIDA (habilita el QR)
                    Servicio->>RepoV: guardar(Venta)
                    RepoV-->>Servicio: Venta
                    Servicio-->>Router: Venta
                    Router-->>Espectador: 200 OK (venta PAGADA, total, entradas con QR)
                end
            end
        end
    end
```

## Lectura del diagrama

- El router arma un `DatosTarjeta` con los datos de la tarjeta del pedido y llama a `iniciar_pago(cliente_id, entrada_ids, DatosTarjeta)`. `PagoRequest` es un esquema HTTP y el servicio no lo conoce.
- El servicio **verifica la disponibilidad antes de llamar a la pasarela** (escenario 3): si falta una entrada, un id está repetido o alguna ya no está disponible, aborta sin tocar nada. Si no, se cobraría por entradas que ya no existen.
- También valida que todas las entradas sean del mismo evento (`EntradasDeDistintosEventos`), porque una venta corresponde a un solo evento.
- Se **reserva** antes de cobrar, para que nadie más tome esas entradas mientras se procesa el pago.
- Si la pasarela rechaza, se **libera**, se guardan las entradas como disponibles y la venta no se guarda: es el escenario 2. Si la pasarela lanza un error inesperado, el servicio también libera las entradas y vuelve a lanzar el error.
- `Venta.calcular_total()` suma `Entrada.precio()`, y cada entrada le pregunta el precio a su `Evento`. Se calcula con la venta ya armada, antes de cobrar.
- Cada cambio de estado lo valida la propia entidad (`Entrada`, `Venta`): si la transición es inválida, lanza `TransicionInvalida`.
- La pasarela es una interfaz. El servicio no sabe si es la simulada o una real (DIP). `get_pasarela` con `Depends` es el único lugar que elige la implementación, y los tests la reemplazan.

## Reserva atómica (resuelto)

`Entrada.reservar()` valida el estado en memoria, y eso solo no alcanza si dos clientes pagan las mismas entradas a la vez: ambos podrían pasar la verificación. La solución implementada es `EntradaRepository.reservar(entradas)`, que ejecuta un `UPDATE` condicional:

- Cambia a `RESERVADA` solo las filas con `estado = DISPONIBLE` y compara el `rowcount` con la cantidad de entradas pedidas.
- Si no coincide, otro pago se adelantó: hace `rollback` y lanza `EntradaNoDisponible`, así que la reserva es todas o ninguna.
- Si coincide, hace `commit` y recién entonces el servicio arma la venta y consulta a la pasarela.
