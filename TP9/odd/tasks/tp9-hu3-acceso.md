# tp9-hu3-acceso

## Objective
Implement HU3 (POST /escanear-acceso): the usher scans a QR; the system validates and registers entry.

## Scope
- In: HU3 scenarios 1-4 of the TP plus the "evento del dia" check (user decision: validate that the event date is today).
- Out: diagram sync (tracked in tp9-hu2-pago.md T3, which now also covers HU3).

## Decisions
- Request body: `{"codigo_qr": "<str>"}`. Response 200: `{"mensaje": "Acceso Permitido", ...}`.
- Check order: QR exists -> estado -> event date.
  - Not found: 404 "Ticket Inválido o Inexistente" (E3).
  - Estado DISPONIBLE or RESERVADA: 400 "Ticket no emitido / Falta de pago" (E4).
  - Estado UTILIZADA: 409 "Entrada ya utilizada", `hora_ingreso` is NOT overwritten (E2).
  - Estado EMITIDA but event date != today: 400 "La entrada no corresponde al evento del día" (design decision, not in TP).
  - Estado EMITIDA and event is today: `hora_ingreso = now`, estado UTILIZADA, 200 (E1).
- "Today" and "now" come from an injectable clock (DIP) so tests are deterministic.
- Registering the entry must be atomic (conditional UPDATE `WHERE estado = 'EMITIDA'`, rowcount check) so two simultaneous scans cannot both enter. Same pattern as HU2 `reservar`.
- Entity owns its rules: `Entrada.registrar_ingreso(hora)` validates EMITIDA -> UTILIZADA; `Evento` answers whether it is the event of the day (Information Expert).

## Tasks
- [x] T1 HU3 implementation (domain, repository, service, router, schemas, exceptions, tests test-first). Route: delegated writer.
- [x] T2 User verifies HU3 in Swagger (needs an event dated today).

## Acceptance criteria
- E1: 200 "Acceso Permitido", hora_ingreso set, estado UTILIZADA.
- E2: 409 "Entrada ya utilizada", original hora_ingreso intact.
- E3: 404 "Ticket Inválido o Inexistente".
- E4: 400 "Ticket no emitido / Falta de pago" for DISPONIBLE and RESERVADA.
- Event not today: 400, entrada stays EMITIDA.
- All pytest tests green (existing 35 + new).

## Progress / evidence
- Delivery: TP9 folder is untracked in git; no commits (ask user first).
- T1 (delegated writer): `.venv/bin/python -m pytest -q` -> 50 passed (35 existing + 15 new in tests/test_escanear_acceso.py). RED observed first (ImportError). Mutation check: removing `Entrada.estado == EMITIDA` from `EntradaRepositorySQL.registrar_ingreso` made 2 atomic tests fail (48 passed); guard restored, 50 passed.
