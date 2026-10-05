# ---- Base image with uv already installed ----
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Faster installs, no bytecode writes inside layer, link mode for cross-fs copies
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# ---- Install deps first (layer-cached when deps don't change) ----
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-install-project --no-dev || uv sync --no-install-project --no-dev

# ---- Copy app source ----
COPY . .

# ---- Install the project itself ----
RUN uv sync --no-dev

# Flask port
EXPOSE 5000

# Run app through uv so it uses the project venv (.venv) automatically
CMD ["uv", "run", "python", "app.py"]
