"""FastAPI app for dietaryindex API MVP."""

from __future__ import annotations

import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.requests import Request

from dietaryindex import __version__
from dietaryindex_api.routers import compute, fii, indices, jobs, mapping, uploads
from dietaryindex_api.settings import settings


logging.basicConfig(
    level=getattr(logging, settings.log_level, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("dietaryindex.api")

app = FastAPI(
    title="DietaryIndex API",
    version=__version__,
    description="Production-oriented API for index metadata, file preview, mapping, computation, result downloads, and FII search.",
)

app.include_router(indices.router, prefix="/v1")
app.include_router(uploads.router, prefix="/v1")
app.include_router(mapping.router, prefix="/v1")
app.include_router(compute.router, prefix="/v1")
app.include_router(jobs.router, prefix="/v1")
app.include_router(fii.router, prefix="/v1")


@app.middleware("http")
async def request_context_and_api_key_guard(request: Request, call_next):
    request_id = request.headers.get("x-request-id", "").strip() or uuid4().hex
    started = perf_counter()
    path = request.url.path
    if settings.require_api_key and path.startswith("/v1"):
        provided = request.headers.get("x-api-key", "").strip()
        if not settings.api_key or provided != settings.api_key:
            response = JSONResponse(
                status_code=401,
                content={
                    "detail": "Unauthorized. Provide a valid x-api-key header.",
                },
            )
        else:
            response = await call_next(request)
    else:
        response = await call_next(request)

    elapsed_ms = round((perf_counter() - started) * 1000, 2)
    response.headers["x-request-id"] = request_id
    logger.info(
        "request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
        request_id,
        request.method,
        path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.get("/")
def root():
    return {
        "name": "DietaryIndex API",
        "version": __version__,
        "docs": "/docs",
        "openapi": "/openapi.json",
        "api_key_required_for_v1": settings.require_api_key,
    }


@app.get("/healthz", tags=["system"])
def healthz():
    return {
        "status": "ok",
        "service": "DietaryIndex API",
        "version": __version__,
        "runtime_dir": str(settings.runtime_dir),
        "api_key_required_for_v1": settings.require_api_key,
    }
