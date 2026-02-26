#!/bin/bash

echo "Waiting for database..."

uv sync --frozen --no-dev

uv run manage.py migrate

echo "Creating superuser (if not exists)..."
uv run manage.py createsuperuser --noinput || true

echo "Starting server..."

exec uv run manage.py runserver 0.0.0.0:8000