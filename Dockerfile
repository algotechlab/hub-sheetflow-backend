FROM python:3.13-slim

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install poetry

RUN pip install asyncpg

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

# desabilita instalação do próprio projeto (evita erro do README)
RUN poetry install --no-interaction --no-ansi --no-root

COPY src /src/src

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
