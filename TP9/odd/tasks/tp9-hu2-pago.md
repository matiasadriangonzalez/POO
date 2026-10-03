# tp9-hu2-pago

## Objective
Implement HU2 (POST /iniciar-pago): pay selected tickets with a card, issue tickets with QR.

## Scope
- In: HU2 scenarios 1-3 of the TP (approved, rejected by gateway, availability lost before gateway).
- Out: HU3 (escanear-acceso), diagram sync (separate task).

## Decisions
- Simulated gateway rejects only `TARJETA_RECHAZADA = "4000000000000002"`; any other card is approved. Rule lives only inside `PasarelaPagoSimulada`; `PagoService` depends on the `PasarelaPago` interface (DIP/OCP). (Confirmed by user; TP does not define it.)
- Messages (section 3 of TP): "Pago denegado", "Los lugares seleccionados ya no se encuentran disponibles".
- HTTP: EntradaNoDisponible 409, PagoDenegado 402.
- Flow per `secuencia_hu2.md`: check availability BEFORE gateway; reserve before charging; rejected => release and do not persist the Venta.
- Reservation must be atomic (conditional UPDATE `WHERE estado = 'DISPONIBLE'`, rowcount check) for the concurrency case.

## Tasks
- [x] T1 HU2 implementation (domain transitions, repositories, exceptions, gateway, PagoService, router, schemas, tests test-first). Route: delegated writer (6+ non-trivial files).
- [x] T2 User verifies HU2 in Swagger (approved card 1111222233334444, rejected 4000000000000002).
- [x] T3 Sync diagrams (HU1 + HU2 + HU3 changes) in diagrama_clases.md / secuencia_hu*.md.

## Acceptance criteria
- Scenario 1: 200, Venta PAGADA, entradas EMITIDA with codigo_qr.
- Scenario 2: "Pago denegado", no Venta persisted, entradas back to DISPONIBLE.
- Scenario 3: entradas not DISPONIBLE => "Los lugares seleccionados ya no se encuentran disponibles", gateway never called.
- All pytest tests green (existing 13 + new).

## Progress / evidence
- Delivery: TP9 folder is entirely untracked in git; no commits made yet (ask user before committing).
- T3 (delegated writer): diagrama_clases.md and secuencia_hu1/2/3.md rewritten against the code; all class/method/exception names confirmed with rg (only conceptual names unmatched: *Router classes, ManejadorExcepciones, which are modules); Mermaid blocks checked by hand (fences balanced, no `;` in diagram text), not render-checked (no mermaid CLI available offline).
- T1: RED observed (ImportError at collection of tests/test_iniciar_pago.py), then GREEN: `python -m pytest -q` from smartticket => 35 passed (13 existing + 22 new). Mutation check: removing `WHERE estado = DISPONIBLE` from `EntradaRepositorySQL.reservar` fails the 2 atomic-reservation tests. Note: an existing `smartticket.db` needs deleting (new `ventas.total` column; `create_all` does not migrate).
