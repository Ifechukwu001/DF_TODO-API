#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install uv
echo "Installing dependencies"
ls -a .venv .venv/bin
uv sync --no-dev
echo "Installing gunicorn and uvicorn"
ls -a .venv .venv/bin
uv pip install gunicorn uvicorn

# Convert static asset files
uv run src/manage.py collectstatic --no-input

# Apply any outstanding database migrations
uv run src/manage.py migrate