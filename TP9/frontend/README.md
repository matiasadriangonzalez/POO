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

The dev server proxies `/api/*` to `http://localhost:8001` (the backend has no CORS), so no extra config is needed.

Other scripts: `npm run build` (typecheck + bundle), `npm run lint`, `npm run preview`.

## Tabs

- **Casos de uso** (default): HU1-HU3 explained with how to test them in the UI, expected results and error cases (marking which ones need Swagger), a suggested test order, useful data and a link to `http://localhost:8001/docs`. Its content lives in `src/content/useCases.ts`.
- **Configuración**: numbered setup sequence 1 Lugar, 2 Sector, 3 Cliente, 4 Evento.
- **Comprar**: HU1 (cotizar) and HU2 (pagar).
- **Puerta**: HU3 (escanear acceso).

The "Cargar datos de ejemplo" button (Casos de uso and Configuración) creates 1 lugar, 1 sector (capacity 100), 1 cliente and 1 evento dated today at 20:00. It only runs when clicked and adds to the existing data (the backend has no delete endpoint).

## Flow to test

1. **Configuración**: create a lugar, then a sector in it, a cliente, and an evento (every sector of the lugar needs a price; use *Hoy 20:00* so the gate accepts it), or press *Cargar datos de ejemplo*.
2. **Comprar**: pick evento, sector and cantidad, press *Cotizar*, choose the cliente and a card, press *Pagar*. You get the entradas with their QR codes.
   - Test cards: `4242424242424242` is approved, `4000000000000002` is rejected by the simulated gateway (402).
3. **Puerta**: click a code from the last purchase (or paste one) and press *Escanear*. The first scan shows "Acceso Permitido"; scanning the same code again shows the backend error (409). The backend only accepts scans on the event's day.
