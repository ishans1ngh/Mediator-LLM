from fastapi import APIRouter, Depends

from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute("SELECT 1")
        return {"status": "ok", "service": "mediator-llm-backend", "database": "connected"}
    except Exception:
        return {"status": "ok", "service": "mediator-llm-backend", "database": "disconnected"}


@router.get("/db")
async def database_health(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}
