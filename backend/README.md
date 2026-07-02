# Backend — Ágora de Paz

API FastAPI en Clean Architecture / DDD. Ver [docs/04-arquitectura.md](../docs/04-arquitectura.md) para el detalle de capas y decisiones de stack.

## Desarrollo local (sin Docker)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API queda en `http://localhost:8000`, con `/health` para verificar que está viva y `/docs` para la documentación interactiva (Swagger).

Los repositorios y el filtro de bien común usan implementaciones en memoria/placeholder por defecto, así que la API funciona sin PostgreSQL ni Ollama corriendo. Para el stack completo:

```bash
docker compose up --build
```

## Tests

```bash
pytest
```
