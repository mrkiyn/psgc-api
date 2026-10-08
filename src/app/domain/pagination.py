"""Pagination value objects shared by repositories and use cases."""

from collections.abc import Sequence
from dataclasses import dataclass
from math import ceil


@dataclass(frozen=True, slots=True)
class PageRequest:
    page: int = 1
    per_page: int = 20

    def __post_init__(self) -> None:
        if self.page < 1:
            raise ValueError("page must be at least 1")
        if self.per_page < 1:
            raise ValueError("per_page must be at least 1")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


@dataclass(frozen=True, slots=True)
class Page[T]:
    items: Sequence[T]
    total: int
    request: PageRequest

    @property
    def total_pages(self) -> int:
        return ceil(self.total / self.request.per_page)

    @classmethod
    def slice(cls, items: Sequence[T], request: PageRequest) -> "Page[T]":
        return cls(
            items=items[request.offset : request.offset + request.per_page],
            total=len(items),
            request=request,
        )
