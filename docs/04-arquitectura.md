# 04 — Arquitectura Técnica

## Decisiones de stack (100% software libre y gratuito)

| Capa | Tecnología | Justificación |
|---|---|---|
| Backend | **Python + FastAPI** | Ecosistema más maduro para orquestación de LLMs locales; integración natural con Ollama / llama.cpp |
| Modelos de IA | **Ollama** (modelos open source locales) | Independencia de APIs comerciales; API compatible con OpenAI consumida localmente |
| Frontend | **Vue** | Ligero, comunidad sólida, preferencia del equipo |
| Base de datos | **PostgreSQL** | Robusta, open source, estándar de facto |
| Contenedores | **Docker + Docker Compose** | Reproducibilidad en desarrollo y producción |
| CI/CD | **GitHub Actions** | Gratuito para repositorios públicos |
| Hosting | Tier gratuito (Railway / Render / Vercel) o VPS propio | Costo cero o mínimo en fase piloto |

## Enfoque arquitectónico

- **Backend monolítico modular** (pragmático): un solo servicio FastAPI bien modularizado internamente por dominios. Si el proyecto crece, los módulos pueden extraerse a servicios independientes.
- **Frontend separado** del backend.
- **Clean Architecture + Domain-Driven Design (DDD)**: el dominio no depende del framework ni de la base de datos.

## Estructura de carpetas del backend

```
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── domain/                  # Lógica pura, sin FastAPI ni SQLAlchemy
│   │   ├── chat/
│   │   │   ├── entities.py      # ChatMessage, Conversation
│   │   │   ├── interfaces.py    # ChatRepository (abstracto)
│   │   │   └── value_objects.py
│   │   ├── consensus/
│   │   │   ├── entities.py      # Consensus, Vote, Cycle
│   │   │   └── interfaces.py
│   │   ├── candidates/
│   │   ├── users/
│   │   └── shared/
│   ├── application/             # Casos de uso y orquestación
│   │   ├── chat/
│   │   │   ├── use_cases.py
│   │   │   └── dtos.py
│   │   ├── consensus/
│   │   │   ├── use_cases.py     # SynthesizeConsensus, VoteConsensus
│   │   │   └── dtos.py
│   │   └── candidates/
│   ├── infrastructure/          # Detalles técnicos
│   │   ├── database/
│   │   │   ├── models.py        # SQLAlchemy ORM
│   │   │   └── repositories.py  # Implementaciones concretas
│   │   └── ai/
│   │       ├── ollama_client.py
│   │       ├── synthesis_engine.py     # Motor de síntesis
│   │       └── common_good_filter.py   # Filtro de bien común (auditable)
│   └── api/                     # Routers FastAPI + schemas Pydantic
│       ├── dependencies.py
│       └── v1/
│           ├── endpoints/
│           │   ├── chat.py
│           │   ├── consensus.py
│           │   ├── votes.py
│           │   └── candidates.py
│           └── schemas.py
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

frontend/                        # Repositorio o carpeta separada (Vue)
```

**Principios por capa:**
- **Domain**: entidades y reglas de negocio puras. Sin imports de frameworks.
- **Application**: casos de uso, DTOs, orquestación entre dominio e infraestructura.
- **Infrastructure**: base de datos, cliente de Ollama, motor de síntesis, filtro de bien común.
- **API**: endpoints HTTP, validación con Pydantic.

## Estado actual

El scaffold de esta estructura ya vive en `backend/` y `frontend/` en la raíz del repositorio (Etapa 2 de la hoja de ruta). Los casos de uso, el motor de síntesis y el filtro de bien común son implementaciones mínimas o stubs: la lógica real de negocio se completa en las Etapas 2 a 4.

---

Ver también: [02-metodologia.md](./02-metodologia.md) · [03-criterios-bien-comun.md](./03-criterios-bien-comun.md) · [05-gobernanza-del-proyecto.md](./05-gobernanza-del-proyecto.md)
