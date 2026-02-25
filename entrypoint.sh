#!/bin/bash

echo "Waiting for database..."

uv sync --frozen --no-dev

uv run manage.py migrate

echo "Starting server..."

exec uv run manage.py runserver 0.0.0.0:8000