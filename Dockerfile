FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY pyproject.toml README.md requirements.txt uv.lock /app/
COPY dietaryindex /app/dietaryindex
COPY dietaryindex_api /app/dietaryindex_api
COPY scripts /app/scripts

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --prefer-binary -e .[all]

EXPOSE 8000

CMD ["uvicorn", "dietaryindex_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
