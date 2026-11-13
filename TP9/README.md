# TP9 – GRASP y SOLID aplicados · SmartTicket

Sistema de venta de entradas y control de acceso. Backend en Python (FastAPI + SQLAlchemy + SQLite) y un front de prueba en React, separados.

## Estructura

| Carpeta / archivo | Contenido |
|---|---|
| `smartticket/` | API REST: `routers/` (HTTP), `services/` (casos de uso), `repositories.py` (persistencia), `models.py` (dominio), `pasarela.py` (pasarela de pago simulada) y `tests/` |
| `frontend/` | Interfaz React + TypeScript para probar las tres historias de usuario |
| `diagrama_clases.md` | Diagramas de clases (dominio, capas, vista general, excepciones) y tabla de justificación GRASP/SOLID |
| `secuencia_hu1.md`, `secuencia_hu2.md`, `secuencia_hu3.md` | Diagramas de secuencia de cada historia |

## Cómo ejecutarlo

Backend (puerto 8001; el front apunta ahí):

```bash
cd smartticket
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --port 8001
```

Swagger: http://localhost:8001/docs

Tests (usan una base SQLite en memoria, no tocan `smartticket.db`):

```bash
cd smartticket
.venv/bin/python -m pytest -q
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Abrir la URL que muestra Vite (por defecto http://localhost:5173). El front llama a `/api`, que Vite redirige a `http://localhost:8001`.

## Historias de usuario y escenarios

| Historia | Endpoint | Escenarios cubiertos |
|---|---|---|
| HU1 – Selección y cotización | `POST /cotizar` | E1 total de 2 × $12.000 = $24.000 (200) · E2 "Capacidad insuficiente" (400) · E3 "Cantidad inválida" para 0 o negativa (400) |
| HU2 – Pago y emisión | `POST /iniciar-pago` | E1 venta Pagada y entradas Emitidas · E2 "Pago denegado" (402) y entradas intactas · E3 entradas ya vendidas, se aborta antes de consultar la pasarela (409) |
| HU3 – Control de acceso | `POST /escanear-acceso` | E1 "Acceso Permitido" y registro de hora · E2 "Entrada ya utilizada" (409) sin pisar la hora original · E3 "Ticket Inválido o Inexistente" (404) · E4 "Ticket no emitido / Falta de pago" (400) |

Además hay CRUD de lugares, sectores, clientes y eventos, y un `POST /webhook-pagos` como esqueleto.

En el front, la pestaña **Casos de uso** ejecuta cada escenario con un clic: prepara los datos, llama a la API y muestra si cumple. Ejecutarlos escribe datos de demostración en `smartticket.db`.

## Decisiones a tener en cuenta

- **Mensaje de HU1 E3:** el enunciado indica dos redacciones (sección 3: "La cantidad de entradas solicitadas debe ser mayor a cero"; sección 6: "Cantidad inválida"). Se usa la de la sección 6.
- **Pasarela simulada:** rechaza solo la tarjeta `4000000000000002`; aprueba el resto. El enunciado no define la regla.
- **Regla adicional en HU3:** solo se admite el ingreso el día del evento (400 "La entrada no corresponde al evento del día"). Es una regla propia que no contradice ningún escenario.
- **Concurrencia:** la reserva de entradas y el registro de ingreso usan un `UPDATE` condicional atómico, de modo que dos compradores o dos escaneos simultáneos no pueden quedarse con la misma entrada.
- **Webhook:** `POST /webhook-pagos` acepta cualquier JSON y responde `{"recibido": true}`. El enunciado no define su comportamiento y el pago actual es sincrónico.
- **Estados:** `Venta` define `Cancelada`, pero ningún flujo del enunciado la utiliza.
