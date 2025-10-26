from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from app.orcastrator.state_graph import build_agent

from app.routes import db, conversations, ingest
from app.orcastrator.embedding import embedding_init
from pathlib import Path
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis






@asynccontextmanager
async def lifespan(app: FastAPI):
    r = redis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(r)
    app.state.vector_store = embedding_init()
    app.state.agent = build_agent(app.state.vector_store)
    UPLOAD_DIR = Path("uploads")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    app.state.UPLOAD_DIR = UPLOAD_DIR 
    yield



app = FastAPI(title="DBA Agent Bot", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, adjust as needed
    allow_headers=["*"],  # Allows all headers, adjust as needed
)
app.add_middleware(GZipMiddleware, minimum_size=1000)  # Compress responses larger than 1000 bytes



#router configuration
app.include_router(db.router, prefix="/db", tags=["Database Operations"])
app.include_router(conversations.router, prefix="/conversations", tags=["Chatbot Operations"])
app.include_router(ingest.router, prefix="/ingest", tags=["Data Ingestion"])


# Health check route
@app.get("/health")
def read_health():
    return {"status": "ok"}