from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat_router, auth_router
from app.core.config import settings
from app.core.database import engine, Base

# Lifespan event to create database tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models import token
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los enrutadores
app.include_router(chat_router.router)
app.include_router(auth_router.router)