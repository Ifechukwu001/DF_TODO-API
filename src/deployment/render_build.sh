#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install uv
uv add uv gunicorn uvicorn
uv sync --no-dev --locked

# Convert static asset files
# uv run src/manage.py collectstatic --no-input

# Apply any outstanding database migrations
uv run --locked src/manage.py migrate