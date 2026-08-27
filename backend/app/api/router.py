from fastapi import APIRouter

from app.api.endpoints import analysis, health, imaging, patients, trials

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(patients.router)
api_router.include_router(imaging.router)
api_router.include_router(trials.router)
api_router.include_router(analysis.router)
