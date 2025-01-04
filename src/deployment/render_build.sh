#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install uv
source .venv/bin/activate
uv sync
uv pip install gunicorn uvicorn

# Convert static asset files
uv run src/manage.py collectstatic --no-input

# Apply any outstanding database migrations
uv run src/manage.py migrate