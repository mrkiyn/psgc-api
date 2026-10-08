"""API version 1.

New v1 routers are included on `api_router` here, so `main.py` only mounts the
`/api/v1` prefix. A future `v2` package can follow the same pattern.
"""

from fastapi import APIRouter

from app.presentation.api.v1.routers import barangays, cities, municipalities, provinces, regions

api_router = APIRouter()
api_router.include_router(regions.router)
api_router.include_router(provinces.router)
api_router.include_router(cities.router)
api_router.include_router(municipalities.router)
api_router.include_router(barangays.router)
