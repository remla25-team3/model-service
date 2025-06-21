FROM python:3.12.9-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12.9-slim

WORKDIR /app

# Copy both the installed packages AND their command-line executables from the builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY app.py .
COPY versioning.py .
COPY src ./src
COPY .release-please-manifest.json .

ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000

# The command to run the application using a production-grade server (Gunicorn).
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]