# SmartTicket frontend

React + Vite + TypeScript UI for the SmartTicket FastAPI backend (`../smartticket`).

## Run

```bash
# 1. Backend (port 8001)
cd ../smartticket
.venv/bin/uvicorn main:app --port 8001

# 2. Frontend (another terminal)
cd frontend
npm install
npm run dev        # http://localhost:5173
```

The dev server proxies `/api/*` to `http://localhost:8001` (the backend has no CORS), so no extra config is needed. Set `API_TARGET` (e.g. `API_TARGET=http://localhost:8002 npm run dev`) to point the proxy at another backend.

Other scripts: `npm run build` (typecheck + bundle), `npm run lint`, `npm run preview`.

## Tabs

- **Casos de uso** (default): pick a user story (HU1-HU3) and a scenario (E1, E2...), read its Dado/Cuando/Entonces and press *Ejecutar escenario*. The app prepares its own demo data, runs the calls against the backend and shows each step (method, path, status, JSON), the expected-vs-actual checks and a PASS/FAIL verdict. *Ejecutar todos los de HUn* / *Ejecutar todo* run several and show an n/m summary. Tickets issued by a scenario can be opened in **Puerta** with one click and also land in "Última compra". A collapsed section lists the cases that only Swagger or the database can reach. **Running scenarios writes demo data to the real database** (lugar "Estadio Demo (escenarios)", cliente demo, and a new "Rock Fest <id>" evento per run; the backend has no delete endpoint).
  - Engine: `src/scenarios/` (pure TypeScript, no React): `fixtures.ts` (idempotent find-or-create + fresh evento), `actions.ts`, `hu1.ts`/`hu2.ts`/`hu3.ts` (scenario definitions with explicit expectations), `context.ts` (records steps and checks), `runner.ts` (`runScenario`, `runAll`; never throws, a network failure becomes a failed result "Backend no disponible en :8001"). The verdict is computed from the recorded checks, never hard-coded.
  - HU3 E4 (ticket never issued) is listed but not automatable: no endpoint exposes the QR of an entrada that was never issued.
  - UI: `src/components/scenarios/`, state in `src/hooks/useScenarioRunner.ts` (held in `App`, so results survive tab switches). Error cases the runner cannot reach live in `src/content/useCases.ts`.
- **Configuración**: numbered setup sequence 1 Lugar, 2 Sector, 3 Cliente, 4 Evento.
- **Comprar**: HU1 (cotizar) and HU2 (pagar).
- **Puerta**: HU3 (escanear acceso).

The "Cargar datos de ejemplo" button (Configuración) creates 1 lugar, 1 sector (capacity 100), 1 cliente and 1 evento dated today at 20:00. It only runs when clicked and adds to the existing data (the backend has no delete endpoint).

## Flow to test

1. **Configuración**: create a lugar, then a sector in it, a cliente, and an evento (every sector of the lugar needs a price; use *Hoy 20:00* so the gate accepts it), or press *Cargar datos de ejemplo*.
2. **Comprar**: pick evento, sector and cantidad, press *Cotizar*, choose the cliente and a card, press *Pagar*. You get the entradas with their QR codes.
   - Test cards: `4242424242424242` is approved, `4000000000000002` is rejected by the simulated gateway (402).
3. **Puerta**: click a code from the last purchase (or paste one) and press *Escanear*. The first scan shows "Acceso Permitido"; scanning the same code again shows the backend error (409). The backend only accepts scans on the event's day.
