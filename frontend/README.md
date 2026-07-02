# Frontend — Ágora de Paz

Chat conversacional en Vue 3 + Vite. Consume la API del [backend](../backend/) en `/api/v1`.

## Desarrollo local

```bash
cd frontend
npm install
npm run dev
```

Corre en `http://localhost:5173` y proxea `/api` hacia `http://localhost:8000` (ver `vite.config.js`). Necesita el backend corriendo en paralelo (`cd backend && uvicorn app.main:app --reload`).
