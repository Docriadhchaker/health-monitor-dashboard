from fastapi import APIRouter

from app.api.v1.endpoints import health, layers, events, sources, regions, search, translations

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(layers.router, prefix="/layers", tags=["layers"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(regions.router, prefix="/regions", tags=["regions"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(translations.router, prefix="/translations", tags=["translations"])
