## Inspired from https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
## Base image is python 3.11 with uv installed already
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

## Set WORKDIR to app
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev


## Copy fastapi code to container
COPY . /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

## OR
# COPY src /app/

ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT []

EXPOSE 9000

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "9000", "src/main.py"]