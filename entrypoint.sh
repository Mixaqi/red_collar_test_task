#!/bin/bash
set -e
echo "Waiting for external services..."

if [[ "$*" == *"runserver"* ]]; then
    echo "Running migrations..."
    uv run manage.py migrate

    echo "Fixing Wagtail page tree..."
    uv run manage.py fixtree

    echo "Creating superuser (if not exists)..."
    uv run manage.py createsuperuser --noinput || true
fi

echo "Starting container process..."
exec "$@"