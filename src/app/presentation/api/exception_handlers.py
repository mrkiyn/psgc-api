"""Maps exceptions to HTTP responses using the `{success, message, data}` envelope."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.domain.exceptions import NotFoundError

logger = logging.getLogger(__name__)


def _error(message: str, *, status_code: int, headers: dict[str, str] | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message, "data": None},
        headers=headers,
    )


def _format_validation_errors(exc: RequestValidationError) -> str:
    details = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error.get("loc", ()) if part != "body")
        details.append(f"{location}: {error.get('msg')}" if location else str(error.get("msg")))
    return "Validation failed: " + "; ".join(details) if details else "Validation failed"


async def _not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return _error(str(exc), status_code=status.HTTP_404_NOT_FOUND)


async def _http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return _error(str(exc.detail), status_code=exc.status_code, headers=getattr(exc, "headers", None))


async def _validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return _error(
        _format_validation_errors(exc),
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


async def _unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return _error("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundError, _not_found_handler)
    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)
    app.add_exception_handler(RequestValidationError, _validation_exception_handler)
    app.add_exception_handler(Exception, _unhandled_exception_handler)
