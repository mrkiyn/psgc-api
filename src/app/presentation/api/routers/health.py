"""Liveness check."""

from fastapi import APIRouter

from app.presentation.api.v1.schemas.common import ApiResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiResponse[None])
async def health() -> ApiResponse[None]:
    return ApiResponse[None](success=True, message="Service is healthy")
