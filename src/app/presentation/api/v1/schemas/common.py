"""Shared response envelopes."""

from collections.abc import Callable
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from app.domain.pagination import Page

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: list[T]
    pagination: PaginationMeta

    @classmethod
    def from_page(
        cls,
        page: Page[Any],
        *,
        message: str,
        serialize: Callable[[Any], T],
    ) -> "PaginatedResponse[T]":
        return cls(
            success=True,
            message=message,
            data=[serialize(item) for item in page.items],
            pagination=PaginationMeta(
                page=page.request.page,
                per_page=page.request.per_page,
                total=page.total,
                total_pages=page.total_pages,
            ),
        )
