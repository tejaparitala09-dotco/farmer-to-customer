import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, check_connection
from routes.auth_routes import router as auth_router
from routes.product_routes import router as product_router
from routes.order_routes import router as order_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Safe startup initialization
    try:
        init_db()
    except Exception as e:
        print(f"[Startup] Warning: database initialization deferred: {e}")
    yield

app = FastAPI(
    title="Farmer to Customer API",
    description="Direct Marketplace connecting local farmers with consumers",
    version="1.0.0",
    lifespan=lifespan
)

# Robust CORS Configuration
configured_origins = os.getenv("FRONTEND_ORIGINS", "")
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:4173",
]

if configured_origins:
    for origin in configured_origins.replace("[", "").replace("]", "").split(","):
        cleaned = origin.strip().rstrip("/")
        if cleaned and cleaned not in allowed_origins:
            allowed_origins.append(cleaned)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if "*" not in allowed_origins else ["*"],
    allow_origin_regex=r"^https:\/\/.*\.vercel\.app$" if "*" not in allowed_origins else None,
    allow_credentials=True if "*" not in allowed_origins else False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(order_router)

@app.get("/")
def root():
    return {
        "service": "Farmer to Customer API",
        "status": "healthy",
        "docs_url": "/docs"
    }

@app.get("/health")
def health():
    db_connected = check_connection()
    return {
        "status": "ok" if db_connected else "degraded",
        "database": "connected" if db_connected else "disconnected"
    }
