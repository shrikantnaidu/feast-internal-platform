FROM python:3.11-slim

# Install uv from the official image — only used during build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy requirements and install with uv
COPY requirements.txt /tmp/requirements.txt
RUN UV_HTTP_TIMEOUT=300 uv pip install --system --no-cache -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

# Render the repository configuration from runtime secrets before each Feast command.
COPY feast-entrypoint.py /usr/local/bin/feast-entrypoint.py

# Copy feature repository
COPY feature_repo/ /opt/feast/feature_repo/

WORKDIR /opt/feast/feature_repo
ENTRYPOINT ["python", "/usr/local/bin/feast-entrypoint.py"]
