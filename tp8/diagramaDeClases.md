```mermaid
classDiagram
    class TerminalPOS {
        -catalogo_productos: CatalogoProductos
        -impresor: ImpresorFacturaConsola
        +iniciar_venta(tipo_comprobante) Factura
        +registrar_item(factura, codigo_producto, cantidad, descuento_producto, descuento_cliente) None
        +finalizar_venta(factura) None
    }

    class CatalogoProductos {
        -_productos: dict
        +registrar_producto(codigo, nombre, precio_base, porcentaje_iva) Producto
        +buscar_por_codigo(codigo) Producto
        +actualizar_precio(codigo, nuevo_precio) None
    }

    class Producto {
        -nombre: str
        -precio_base: float
        -porcentaje_iva: float
    }

    class Factura {
        -tipo_comprobante: str
        -lineas: list
        +agregar_linea(producto, cantidad, descuento_producto, descuento_cliente) LineaFactura
        +calcular_total_neto() float
        +calcular_total_iva() float
        +calcular_total_iva_por_tasa(tasa) float
        +calcular_total_final() float
    }

    class LineaFactura {
        -cantidad: int
        -producto: Producto
        -precio_unitario_historico: float
        -porcentaje_iva_historico: float
        -descuento_producto: Descuento
        -descuento_cliente: Descuento
        +calcular_subtotal_bruto() float
        +calcular_subtotal_tras_descuento_producto() float
        +calcular_subtotal_neto_con_descuento() float
        +calcular_monto_iva() float
        +calcular_total_linea() float
    }

    class Descuento {
        <<abstract>>
        +aplicar(monto_base, cantidad) float
    }

    class SinDescuento {
        +aplicar(monto_base, cantidad) float
    }

    class Descuento3x2 {
        +aplicar(monto_base, cantidad) float
    }

    class DescuentoPorcentaje {
        -porcentaje: float
        +aplicar(monto_base, cantidad) float
    }

    class DescuentoPorVolumen {
        -cantidad_minima: int
        -porcentaje: float
        +aplicar(monto_base, cantidad) float
    }

    class ImpresorFacturaConsola {
        +imprimir(factura) None
    }

    TerminalPOS "1" --> "1" CatalogoProductos : usa
    TerminalPOS ..> Factura : crea
    TerminalPOS ..> ImpresorFacturaConsola : usa
    CatalogoProductos "1" o-- "*" Producto : gestiona y crea
    Factura "1" o-- "*" LineaFactura : contiene y crea
    LineaFactura "*" --> "1" Producto : refiere a
    LineaFactura "1" --> "2" Descuento : usa
    ImpresorFacturaConsola ..> Factura : usa
    Descuento <|.. SinDescuento : implementa
    Descuento <|.. Descuento3x2 : implementa
    Descuento <|.. DescuentoPorcentaje : implementa
    Descuento <|.. DescuentoPorVolumen : implementa
```

## Notas de diseño

- **Atributos históricos (Parte 1, Punto 1):** `LineaFactura` guarda `precio_unitario_historico` y `porcentaje_iva_historico`, copiados de `Producto` en el momento de la venta. No hay ninguna flecha entre `Factura` y `Producto` directamente.
- **Ley de Demeter (Parte 1, Punto 2):** `Factura` solo se relaciona con `LineaFactura`. Es `LineaFactura` quien se relaciona con `Producto`, no `Factura`.
- **Fabricación Pura (Parte 2, Punto 4):** `ImpresorFacturaConsola` no representa ningún concepto del negocio de facturación; existe únicamente para resolver la presentación por consola.
- **Polimorfismo de descuentos (Parte 3, Punto 8):** `Descuento` es abstracta, con cuatro implementaciones concretas. `LineaFactura` recibe DOS descuentos (`descuento_producto` y `descuento_cliente`), aplicados en cadena, siguiendo la granularidad definida en el Punto 6 (descuentos de producto a nivel línea, descuentos de cliente/volumen también inyectados por línea para preservar la matemática del IVA por tasa).
- **Patrón Creador (Parte 4, Punto 9):** `Factura` crea sus propias `LineaFactura` (método `agregar_linea`), `TerminalPOS` crea la `Factura`, y `CatalogoProductos` crea y gestiona los `Producto`.