from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.redis import redis_ping
from app.db.session import get_db

app = FastAPI(
    title="HealthMonitor API",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Liveness/readiness: DB and Redis must be reachable."""
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass
    redis_ok = redis_ping()
    status = "ok" if (db_ok and redis_ok) else "degraded"
    payload = {
        "status": status,
        "database": "ok" if db_ok else "error",
        "redis": "ok" if redis_ok else "error",
    }
    status_code = 200 if status == "ok" else 503
    return JSONResponse(content=payload, status_code=status_code)
