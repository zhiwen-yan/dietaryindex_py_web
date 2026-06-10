FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true

WORKDIR /app

COPY pyproject.toml README.md requirements.txt uv.lock /app/
COPY dietaryindex /app/dietaryindex
COPY scripts /app/scripts
COPY streamlit_app /app/streamlit_app
COPY streamlit_app/.streamlit /app/streamlit_app/.streamlit

RUN pip install --upgrade pip && \
    pip install -e .[streamlit,adapters]

WORKDIR /app/streamlit_app

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "app.py"]
