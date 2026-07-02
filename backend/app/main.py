from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import candidates, chat, consensus, votes
from app.core.config import get_settings
from app.infrastructure.database.session import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.repository_backend == "postgres":
        init_db(settings)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix=settings.api_v1_prefix)
app.include_router(consensus.router, prefix=settings.api_v1_prefix)
app.include_router(votes.router, prefix=settings.api_v1_prefix)
app.include_router(candidates.router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}
