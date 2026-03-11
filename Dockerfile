FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y  --no-install-recommends \
        libpq-dev \
        gdal-bin \
        binutils \
        libproj-dev \
        curl \
        bash \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser \
    && curl -Ls https://astral.sh/uv/install.sh | bash \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mkdir -p /home/appuser/app \
    && chown appuser:appuser /home/appuser/app

USER appuser
WORKDIR /home/appuser/app

COPY --chown=appuser:appuser pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY --chown=appuser:appuser . .

USER root
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
USER appuser

ENTRYPOINT ["/entrypoint.sh"]