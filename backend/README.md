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

Por defecto (`REPOSITORY_BACKEND=memory`) los repositorios son en memoria, así que la API arranca y los tests corren sin PostgreSQL ni Ollama. Para el stack completo (Postgres real + Ollama):

```bash
docker compose up --build
```

o localmente, copiando `.env.example` a `.env` y ajustando `REPOSITORY_BACKEND=postgres` con un PostgreSQL corriendo (las tablas se crean automáticamente al arrancar).

### Ollama

El chat conversacional (`POST /api/v1/chat/conversations/{id}/messages`), el motor de síntesis y el filtro de bien común llaman a un servidor [Ollama](https://ollama.com) local (`OLLAMA_BASE_URL`, por defecto `http://localhost:11434`). Sin Ollama corriendo, esos endpoints devuelven error 500; el resto de la API (crear conversación, consultar consensos, votar) funciona igual.

```bash
ollama serve
ollama pull llama3.1   # o el modelo configurado en OLLAMA_MODEL
```

## Tests

```bash
pytest
```

`tests/test_repositories_postgres.py` se salta automáticamente si no hay PostgreSQL disponible en `DATABASE_URL`; el resto de tests usan los repositorios en memoria y un asistente/filtro/motor de síntesis falsos (sin depender de Ollama).
