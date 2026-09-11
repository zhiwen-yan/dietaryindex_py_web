"""In-memory job manager for API MVP."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import UTC, datetime
import logging
from threading import Lock
from uuid import uuid4

from dietaryindex.service.compute import run_compute, run_multi_cycle_compute
from dietaryindex_api.storage import create_result_dir


_executor = ThreadPoolExecutor(max_workers=2)
_jobs: dict[str, dict] = {}
_lock = Lock()
logger = logging.getLogger("dietaryindex.jobs")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def submit_compute_job(
    *,
    index_key: str,
    mode: str,
    file_path: str | None = None,
    file_paths: dict | None = None,
    mapping: dict | None = None,
    options: dict | None = None,
    cycles: list[dict] | None = None,
) -> dict:
    job_id = uuid4().hex
    with _lock:
        _jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "created_at": _utc_now(),
            "index_key": index_key,
            "mode": mode,
            "file_path": file_path,
            "file_paths": file_paths,
            "mapping": mapping or {},
            "options": options or {},
            "cycles": cycles or [],
            "result": None,
            "error": None,
        }

    def _runner():
        with _lock:
            _jobs[job_id]["status"] = "running"
            _jobs[job_id]["started_at"] = _utc_now()
        try:
            if cycles:
                result = run_multi_cycle_compute(
                    index_key=index_key,
                    mode=mode,
                    cycles=cycles,
                    options=options or mapping or {},
                    output_dir=create_result_dir(job_id),
                )
            else:
                result = run_compute(
                    index_key=index_key,
                    mode=mode,
                    file_path=file_path,
                    file_paths=file_paths,
                    mapping=mapping or {},
                    options=options or {},
                    output_dir=create_result_dir(job_id),
                )
            with _lock:
                _jobs[job_id]["status"] = "succeeded"
                _jobs[job_id]["finished_at"] = _utc_now()
                _jobs[job_id]["result"] = result
        except Exception as exc:
            logger.exception("compute_job_failed job_id=%s index=%s mode=%s", job_id, index_key, mode)
            with _lock:
                _jobs[job_id]["status"] = "failed"
                _jobs[job_id]["finished_at"] = _utc_now()
                _jobs[job_id]["error"] = {"type": type(exc).__name__, "message": str(exc)}

    _executor.submit(_runner)
    return get_job_view(job_id)


def get_job(job_id: str) -> dict:
    with _lock:
        if job_id not in _jobs:
            raise KeyError(job_id)
        return dict(_jobs[job_id])


def get_job_view(job_id: str) -> dict:
    """Return the public job representation without local filesystem paths."""

    job = get_job(job_id)
    payload = {
        key: deepcopy(value)
        for key, value in job.items()
        if key not in {"file_path", "file_paths", "cycles"}
    }
    result = payload.get("result")
    if isinstance(result, dict):
        result.pop("files", None)
        if job.get("result", {}).get("files"):
            result["downloads"] = {
                "csv": f"/v1/jobs/{job_id}/download?format=csv",
                "xlsx": f"/v1/jobs/{job_id}/download?format=xlsx",
            }
    return payload
