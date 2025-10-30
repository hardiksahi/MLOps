## https://github.com/hardiksahi/MLOps/blob/main/tutorials/docker/fastapi/Dockerfile
## https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
## Base image with uv installed
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

## Set WORKDIR
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin


## Install dependencies using uv sync from pyproject.toml
## Bind mount uv.lock and pyproject.toml from local to 
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

## Copy src folder to docker container.
COPY --chown=nonroot:nonroot src /app
COPY dist /app/dist

## Unzip .gz file to location /app
RUN tar -xzf /app/dist/conf*.gz -C /app && rm /app/dist/conf*.gz

COPY ./pyproject.toml ./pyproject.toml
COPY ./uv.lock ./uv.lock
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

RUN uv add /app/dist/kedro2package*.whl

# # Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# # Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

USER nonroot

CMD ["sh", "entrypoint.sh"]


# CMD ["bash"]
