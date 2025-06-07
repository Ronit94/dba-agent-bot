from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.routes import db, conversations

app = FastAPI(title="DBA Agent Bot", version="1.0.0")

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



# Health check route
@app.get("/health")
def read_health():
    return {"status": "ok"}