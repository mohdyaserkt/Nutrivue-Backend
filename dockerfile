# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.7.1

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./

# Install dependencies (including psycopg2)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi


# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install libpq for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy installed dependencies
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Run migrations on startup (if using alembic)
COPY ./migrations /app/migrations
RUN if [ -f alembic.ini ]; then \
      pip install alembic && \
      alembic upgrade head; \
    fi

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]